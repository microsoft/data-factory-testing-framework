from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationError,
    ExpressionEvaluationInvalidChildTypeError,
)
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult

from .expression_rule_evaluator import ExpressionRuleEvaluator


class LiteralInterpolationExpressionRuleEvaluator(ExpressionRuleEvaluator):
    def __init__(self, tree: Tree) -> None:
        """Initializes the expression rule evaluator."""
        super().__init__(tree)

        for index, child in enumerate(self.children):
            if not isinstance(child, (ExpressionRuleEvaluator, EvaluationResult)):
                raise ExpressionEvaluationInvalidChildTypeError(
                    child_index=index,
                    expected_types=(ExpressionRuleEvaluator, EvaluationResult),
                    actual_type=type(child),
                )

        self.literal_interpolation_items = self.children

    def evaluate(self) -> EvaluationResult:
        evaluation_result = ""
        for item in self.literal_interpolation_items:
            value = self.evaluate_child(item).value
            if not isinstance(value, (str, int, float, bool, None)):
                raise ExpressionEvaluationError("Literal interpolation only supports string, int, float, bool and None")
            evaluation_result += str(value)
        return EvaluationResult(evaluation_result)
