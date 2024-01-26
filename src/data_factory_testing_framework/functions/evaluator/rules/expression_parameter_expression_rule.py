from lark import Tree

from data_factory_testing_framework.functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression

from .expression_rule import ExpressionRuleEvaluator


class ExpressionParameterExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) != 1:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=1, actual=len(self.children))

        if not isinstance(self.children[0], (EvaluatedExpression, ExpressionRuleEvaluator)):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0,
                expected_types=(EvaluatedExpression, ExpressionRuleEvaluator),
                actual_type=type(self.children[0]),
            )

    def evaluate(self) -> EvaluatedExpression:
        if isinstance(self.children[0], EvaluatedExpression):
            return self.children[0]

        return self.children[0].evaluate()
