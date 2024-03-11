from data_factory_testing_framework._expression_runtime.data_factory_expression.exceptions import (
    ExpressionEvaluationError,
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._expression_runtime.data_factory_expression.rules.expression_rule_evaluator import (
    EvaluationResult,
)
from data_factory_testing_framework.state import RunParameterType
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState
from lark import Token, Tree

from .expression_rule_evaluator import ExpressionRuleEvaluator


class PipelineReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState = None) -> None:
        """Initialize the expression rule."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 2:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=2, actual=len(self.children))

        if not isinstance(self.children[0], Token):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=Token, actual_type=type(self.children[0])
            )

        if not isinstance(self.children[1], Token):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=1, expected_types=Token, actual_type=type(self.children[1])
            )

        self.parameter_type = self._get_run_parameter_type(self.children[0].value)
        self.parameter_name = self.children[1].value

    def evaluate(self) -> EvaluationResult:
        result = self.state.get_parameter_by_type_and_name(
            self.parameter_type,
            self.parameter_name,
        )
        return EvaluationResult(result)

    @staticmethod
    def _get_run_parameter_type(value: str) -> RunParameterType:
        if value == "parameters":
            return RunParameterType.Pipeline
        elif value == "globalParameters":
            return RunParameterType.Global
        else:
            raise ExpressionEvaluationError(f"Unsupported run parameter type: {value}")
