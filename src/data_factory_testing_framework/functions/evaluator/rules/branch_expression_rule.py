from typing import Union

from lark import Tree

from data_factory_testing_framework.exceptions.expression_evaluation_error import ExpressionEvaluationError
from data_factory_testing_framework.functions.evaluator.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
    ExpressionEvaluationInvalidNumberOfChildrenError,
)
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression

from .expression_rule import ExpressionRuleEvaluator


class BranchExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) != 3:
            raise ExpressionEvaluationInvalidNumberOfChildrenError(required=3, actual=len(self.children))

        for i, child in enumerate(self.children):
            self._check_child_type(child, i)

    def _check_child_type(self, child: Union[EvaluatedExpression, ExpressionRuleEvaluator], child_index: int) -> None:
        if not isinstance(child, (EvaluatedExpression, ExpressionRuleEvaluator)):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=child_index,
                expected_types=(EvaluatedExpression, ExpressionRuleEvaluator),
                actual_type=type(child),
            )

    def _evaluate_child(self, child: Union[EvaluatedExpression, ExpressionRuleEvaluator]) -> EvaluatedExpression:
        if isinstance(child, ExpressionRuleEvaluator):
            return child.evaluate()
        else:
            return child.value

    def evaluate(self) -> EvaluatedExpression:
        expression_result = self._evaluate_child(self.children[0])

        if not isinstance(expression_result, EvaluatedExpression) and not isinstance(expression_result.value, bool):
            raise ExpressionEvaluationError("Expression result must be a boolean value.")

        if expression_result.value:
            return self._evaluate_child(self.children[1])
        else:
            return self._evaluate_child(self.children[2])
