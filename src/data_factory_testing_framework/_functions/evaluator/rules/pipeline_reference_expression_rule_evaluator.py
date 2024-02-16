from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState

from .expression_rule_evaluator import ExpressionRuleEvaluator


class PipelineReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState = None) -> None:
        """Initialize the expression rule."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 2:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=2, actual=len(self.children))

        if not isinstance(self.children[0], EvaluationResult):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=EvaluationResult, actual_type=type(self.children[0])
            )

        if not isinstance(self.children[1], EvaluationResult):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=1, expected_types=EvaluationResult, actual_type=type(self.children[1])
            )
        self.parameter_type = self.children[0].value
        self.parameter_name = self.children[1].value

    def evaluate(self) -> EvaluationResult:
        result = self.state.get_parameter_by_type_and_name(
            self.parameter_type,
            self.parameter_name,
        )
        return EvaluationResult(result)
