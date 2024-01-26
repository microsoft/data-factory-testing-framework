from lark import Tree

from data_factory_testing_framework.functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression
from data_factory_testing_framework.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.state.run_parameter_type import RunParameterType

from .expression_rule import ExpressionRuleEvaluator


class LinkedServiceReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState) -> None:
        """Initialize expression rule evaluator."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 1:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=1, actual=len(self.children))

        if not isinstance(self.children[0], EvaluatedExpression):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=EvaluatedExpression, actual_type=type(self.children[0])
            )

    def evaluate(self) -> EvaluatedExpression:
        parameter_name = self.children[0].value
        activity = self.state.get_parameter_by_type_and_name(RunParameterType.LinkedService, parameter_name)
        return EvaluatedExpression(activity)
