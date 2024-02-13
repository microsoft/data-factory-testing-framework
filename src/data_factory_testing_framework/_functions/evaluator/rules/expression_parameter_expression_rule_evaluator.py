from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult

from .expression_rule_evaluator import ExpressionRuleEvaluator


class ExpressionParameterExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) != 1:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=1, actual=len(self.children))

        if not isinstance(self.children[0], (EvaluationResult, ExpressionRuleEvaluator)):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0,
                expected_types=(EvaluationResult, ExpressionRuleEvaluator),
                actual_type=type(self.children[0]),
            )
        self.parameter_name_expression = self.children[0]

    def evaluate(self) -> EvaluationResult:
        return self.evaluate_child(self.parameter_name_expression)
