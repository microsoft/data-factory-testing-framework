from data_factory_testing_framework._expression_runtime.data_factory_expression.exceptions import (
    ExpressionEvaluationError,
    ExpressionEvaluationInvalidChildTypeError,
)
from data_factory_testing_framework._expression_runtime.data_factory_expression.rules.expression_rule_evaluator import (
    EvaluationResult,
    evaluate_child,
)
from lark import Token, Tree

from .expression_rule_evaluator import ExpressionRuleEvaluator


class LiteralInterpolationExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        for index, child in enumerate(self.children):
            if not isinstance(child, (ExpressionRuleEvaluator, Token)):
                raise ExpressionEvaluationInvalidChildTypeError(
                    child_index=index,
                    expected_types=(ExpressionRuleEvaluator, Token),
                    actual_type=type(child),
                )

        self.literal_interpolation_items = self.children

    def evaluate(self) -> EvaluationResult:
        evaluation_result = ""
        for item in self.literal_interpolation_items:
            value = evaluate_child(item).value
            if not isinstance(value, (str, int, float, bool, None)):
                raise ExpressionEvaluationError("Literal interpolation only supports string, int, float, bool and None")

            if item.type == "EXPRESSION_STRING":
                evaluation_result += str(value[1:-1])
            else:
                evaluation_result += str(value)
        return EvaluationResult(evaluation_result)
