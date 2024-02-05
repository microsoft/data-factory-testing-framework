from lark import Tree

from data_factory_testing_framework.exceptions.expression_evaluation_error import ExpressionEvaluationError
from data_factory_testing_framework.functions.evaluator.exceptions import ExpressionEvaluationInvalidChildTypeError
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression

from .expression_rule import ExpressionRuleEvaluator


class LiteralInterpolationExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        for index, child in enumerate(self.children):
            if not isinstance(child, (ExpressionRuleEvaluator, EvaluatedExpression)):
                raise ExpressionEvaluationInvalidChildTypeError(
                    child_index=index,
                    expected_types=(ExpressionRuleEvaluator, EvaluatedExpression),
                    actual_type=type(child),
                )

        self.literal_interpolation_items = self.children

    def evaluate(self) -> EvaluatedExpression:
        evaluation_result = ""
        for item in self.literal_interpolation_items:
            value = self.ensure_evaluated_expression(item).value
            if not isinstance(value, (str, int, float, bool, None)):
                raise ExpressionEvaluationError("Literal interpolation only supports string, int, float, bool and None")
            evaluation_result += str(value)
        return EvaluatedExpression(evaluation_result)
