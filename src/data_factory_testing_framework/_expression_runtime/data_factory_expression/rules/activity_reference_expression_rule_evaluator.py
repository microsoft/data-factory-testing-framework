from data_factory_testing_framework._expression_runtime.data_factory_expression.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._expression_runtime.data_factory_expression.rules.expression_rule_evaluator import (
    EvaluationResult,
)
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState
from lark import Token, Tree

from .expression_rule_evaluator import ExpressionRuleEvaluator


class ActivityReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState) -> None:
        """Initialize expression rule evaluator."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 1:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=1, actual=len(self.children))

        if not isinstance(self.children[0], Token):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=Token, actual_type=type(self.children[0])
            )

        self.activity_name = self.children[0].value[1:-1]

    def evaluate(self) -> EvaluationResult:
        activity_result = self.state.get_activity_result_by_name(self.activity_name)
        return EvaluationResult(
            {
                "output": activity_result["output"],
                "status": activity_result["status"],
            }
        )
