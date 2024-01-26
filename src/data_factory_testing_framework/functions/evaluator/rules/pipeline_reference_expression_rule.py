from lark import Tree

from data_factory_testing_framework.functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression
from data_factory_testing_framework.state.pipeline_run_state import PipelineRunState

from .expression_rule import ExpressionRuleEvaluator


class PipelineReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState = None) -> None:
        """Initialize the expression rule."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 2:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=2, actual=len(self.children))

        if not isinstance(self.children[0], EvaluatedExpression):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=EvaluatedExpression, actual_type=type(self.children[0])
            )

        if not isinstance(self.children[1], EvaluatedExpression):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=1, expected_types=EvaluatedExpression, actual_type=type(self.children[1])
            )

    def evaluate(self) -> EvaluatedExpression:
        parameter_type: EvaluatedExpression = self.children[0]
        parameter_name: EvaluatedExpression = self.children[1]
        result = self.state.get_parameter_by_type_and_name(
            parameter_type.value,
            parameter_name.value,
        )
        return EvaluatedExpression(result)
