from lark import Tree

from data_factory_testing_framework.exceptions.expression_evaluation_error import ExpressionEvaluationError
from data_factory_testing_framework.functions.evaluator.exceptions import ExpressionEvaluationInvalidChildTypeError
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression

from .expression_rule import ExpressionRuleEvaluator


class EvaluationExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        if len(self.children) < 1:
            raise ExpressionEvaluationError(
                f"Invalid number of children. Minimum required: 1, Actual: {len(self.children)}"
            )

        if not isinstance(self.children[0], ExpressionRuleEvaluator):
            raise ExpressionEvaluationInvalidChildTypeError(
                child_index=0, expected_types=ExpressionRuleEvaluator, actual_type=type(self.children[0])
            )

    def evaluate(self) -> EvaluatedExpression:
        expression = self.children[0]
        accessors = self.children[1:]

        expression_value = expression.evaluate()
        if not isinstance(expression_value, EvaluatedExpression):
            raise ExpressionEvaluationError("Not an evaluated expression.")

        current_value = expression_value.value
        for accessor in accessors:
            if not isinstance(accessor, EvaluatedExpression):
                raise ExpressionEvaluationError("Not an evaluated expression.")

            current_value = current_value[accessor.value]

        return EvaluatedExpression(current_value)
