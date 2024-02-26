from typing import Union

from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationError,
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult

from .expression_rule_evaluator import ExpressionRuleEvaluator


class LogicalBoolExpressionEvaluator(ExpressionRuleEvaluator):
    OR = "or"
    AND = "and"

    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) != 3:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=3, actual=len(self.children))

        if not isinstance(self.children[0], EvaluationResult):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0,
                expected_types=(EvaluationResult,),
                actual_type=type(self.children[0]),
            )

        for i, child in enumerate(self.children[1:]):
            self._check_child_type(child, i)

        if self.children[0].value not in (self.OR, self.AND):
            self._raise_invalid_operator(self.children[0].value)

        self.logical_operator = self.children[0].value
        self.left_expression = self.children[1]
        self.right_expression = self.children[2]

    def _raise_invalid_operator(self, logical_operator: str) -> None:
        raise ExpressionEvaluationError(f"Invalid logical operator: {logical_operator}")

    def _check_child_type(self, child: Union[EvaluationResult, ExpressionRuleEvaluator], child_index: int) -> None:
        if not isinstance(child, (ExpressionRuleEvaluator, EvaluationResult)):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=child_index,
                expected_types=(ExpressionRuleEvaluator, EvaluationResult),
                actual_type=type(child),
            )

    def evaluate(self) -> EvaluationResult:
        if self.logical_operator == self.OR:
            value = self._evaluate_expression(self.left_expression) or self._evaluate_expression(self.right_expression)
        elif self.logical_operator == self.AND:
            value = self._evaluate_expression(self.left_expression) and self._evaluate_expression(self.right_expression)
        else:
            self._raise_invalid_operator(self.logical_operator)
        return EvaluationResult(value)

    def _evaluate_expression(self, expression: Union[ExpressionRuleEvaluator, EvaluationResult]) -> bool:
        result = self.evaluate_child(expression)
        if not isinstance(result.value, bool):
            raise ExpressionEvaluationError(f"Evaluating expression resulted in non-boolean value: {result.value}")

        return result.value
