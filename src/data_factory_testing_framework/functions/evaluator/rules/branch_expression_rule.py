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

        self.condition = self.children[0]
        self.true_expression_branch = self.children[1]
        self.false_expression_branch = self.children[2]

    def _check_child_type(self, child: Union[EvaluatedExpression, ExpressionRuleEvaluator], child_index: int) -> None:
        if not isinstance(child, (EvaluatedExpression, ExpressionRuleEvaluator)):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=child_index,
                expected_types=(EvaluatedExpression, ExpressionRuleEvaluator),
                actual_type=type(child),
            )

    def evaluate(self) -> EvaluatedExpression:
        condition_result = self._evaluate_child(self.condition)

        if not isinstance(condition_result, EvaluatedExpression) and not isinstance(condition_result.value, bool):
            raise ExpressionEvaluationError("Expression result must be a boolean value.")

        if condition_result.value:
            return self._evaluate_child(self.true_expression_branch)
        else:
            return self._evaluate_child(self.false_expression_branch)

    def _evaluate_child(self, child: Union[EvaluatedExpression, ExpressionRuleEvaluator]) -> EvaluatedExpression:
        if isinstance(child, ExpressionRuleEvaluator):
            return child.evaluate()
        else:
            return child.value
