from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult
from data_factory_testing_framework.exceptions import StateIterationItemNotSetError
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState

from .expression_rule_evaluator import ExpressionRuleEvaluator


class ItemReferenceExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree, state: PipelineRunState) -> None:
        """Initialize expression rule evaluator."""
        super().__init__(tree)
        self.state: PipelineRunState = state

        if len(self.children) != 0:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=0, actual=len(self.children))

    def evaluate(self) -> EvaluationResult:
        item = self.state.iteration_item
        if item is None:
            raise StateIterationItemNotSetError()
        return EvaluationResult(item)
