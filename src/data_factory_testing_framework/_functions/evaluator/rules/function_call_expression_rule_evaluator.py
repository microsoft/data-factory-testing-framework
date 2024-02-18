import inspect
from typing import Callable, Union

from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationError,
    ExpressionEvaluationInvalidChildTypeError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import (
    EvaluationResult,
    ExpressionRuleEvaluator,
)
from data_factory_testing_framework._functions.functions_repository import FunctionsRepository


class FunctionCallExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) < 1:
            raise ExpressionEvaluationError(
                f"Invalid number of children. Minimum required: 1, Actual: {len(self.children)}"
            )

        if not isinstance(self.children[0], EvaluationResult):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=EvaluationResult, actual_type=type(self.children[0])
            )

        for i, child in enumerate(self.children[1:]):
            if isinstance(child, (EvaluationResult, ExpressionRuleEvaluator)):
                continue

            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=i, expected_types=(EvaluationResult, ExpressionRuleEvaluator), actual_type=type(child)
            )

        self.function_name = self.children[0].value
        self.parameters = self.children[1:]

    def evaluate(self) -> EvaluationResult:
        evaluated_parameters = self._evaluated_parameters(self.parameters)
        function: Callable = FunctionsRepository._functions.get(self.function_name)

        pos_or_kw_params, var_pos_params = self._build_function_call_parameters(function, evaluated_parameters)
        result = function(*pos_or_kw_params, *var_pos_params)

        return EvaluationResult(result)

    def _build_function_call_parameters(
        self, function: Callable, parameters: list[Union[EvaluationResult, ExpressionRuleEvaluator]]
    ) -> tuple[
        Union[
            list[Union[EvaluationResult, ExpressionRuleEvaluator]],
            list[Union[EvaluationResult, ExpressionRuleEvaluator]],
        ]
    ]:
        function_signature = inspect.signature(function)
        pos_or_keyword_parameters = [
            param
            for param in function_signature.parameters.values()
            if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ]

        pos_or_keyword_values = parameters[: len(pos_or_keyword_parameters)]
        var_positional_values = parameters[len(pos_or_keyword_parameters) :]
        # TODO: implement automatic conversion of parameters based on type hints
        return pos_or_keyword_values, var_positional_values

    def _evaluated_parameters(
        self, parameters: list[Union[EvaluationResult, ExpressionRuleEvaluator]]
    ) -> list[EvaluationResult]:
        evaluated_parameters = []
        for p in parameters:
            evaluated_expression = self.evaluate_child(p)
            evaluated_parameters.append(evaluated_expression.value)
        return evaluated_parameters
