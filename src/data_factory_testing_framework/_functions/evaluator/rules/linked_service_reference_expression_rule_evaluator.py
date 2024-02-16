from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState
from data_factory_testing_framework.state._run_parameter_type import RunParameterType

from .expression_rule_evaluator import ExpressionRuleEvaluator


class LinkedServiceReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState) -> None:
        """Initialize expression rule evaluator."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 1:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=1, actual=len(self.children))

        if not isinstance(self.children[0], EvaluationResult):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=EvaluationResult, actual_type=type(self.children[0])
            )

        self.parameter_name = self.children[0].value

    def evaluate(self) -> EvaluationResult:
        parameter = self.state.get_parameter_by_type_and_name(RunParameterType.LinkedService, self.parameter_name)
        return EvaluationResult(parameter)
