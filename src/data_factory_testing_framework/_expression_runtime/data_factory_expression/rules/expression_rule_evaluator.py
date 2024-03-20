import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union

from data_factory_testing_framework._expression_runtime.data_factory_expression.exceptions import (
    ExpressionEvaluationInvalidChildTypeError,
)
from lark import Token, Tree


@dataclass
class EvaluationResult:
    """Evaluated expression data class."""

    value: Any


def evaluate_child(child: Union[EvaluationResult, "ExpressionRuleEvaluator"]) -> EvaluationResult:
    """Evaluates a child of the expression rule.

    If the child is an expression rule evaluator, it is evaluated so that the result is always an EvaluationResult.
    """
    if isinstance(child, ExpressionRuleEvaluator):
        return child.evaluate()
    else:
        return child


class ExpressionRuleEvaluator(ABC):
    """Abstract class for expression rule evaluators.

    Implementations of this class should evaluate the expression rule and return an evaluated expression.
    Decorates the lark Tree class to provide a tree structure for the expression rule.
    The base class implementation checks that the children are of the correct type.
    """

    def __init__(self, tree: Tree["ExpressionRuleEvaluator"]) -> None:
        """Initializes the expression rule."""
        self._tree = tree

        # check that children are of the correct type
        if not all(isinstance(child, (Token, EvaluationResult, ExpressionRuleEvaluator)) for child in self.children):
            raise ExpressionEvaluationInvalidChildTypeError(
                expected_types=(EvaluationResult, ExpressionRuleEvaluator),
                actual_types=[type(child) for child in self.children],
            )

    @abstractmethod
    def evaluate(self) -> EvaluationResult:
        """Evaluates the expression rule."""
        pass

    def evaluate_and_transform(self) -> Union[Token, Tree]:
        """Evaluates the expression rule and reconstructs the tree."""
        # value = self.evaluate().value
        return self.evaluate()

    @property
    def children(self) -> list[Union["ExpressionRuleEvaluator", EvaluationResult]]:
        """Returns the children of the expression rule."""
        return self._tree.children

    @staticmethod
    def _reconstruct_expression_tree_from_value(value: Any) -> Union[Token, Tree]:  # type: ignore # noqa: ANN401
        """Reconstructs the expression tree from the value."""
        if isinstance(value, str):
            return Token("EXPRESSION_STRING", f"'{value}'")
        if isinstance(value, int):
            return Token("EXPRESSION_INTEGER", value)
        if isinstance(value, float):
            return Token("EXPRESSION_FLOAT", value)
        if isinstance(value, bool):
            return Token("EXPRESSION_BOOLEAN", value)
        if isinstance(value, dict) or isinstance(value, list):
            return Tree(
                Token("RULE", "expression_function_call"),
                [Token("EXPRESSION_FUNCTION_NAME", "json"), Token("EXPRESSION_STRING", f"'{json.dumps(value)}'")],
            )
        if value is None:
            return Token("EXPRESSION_NULL", None)

        raise ValueError(f"Unsupported result type: {type(value)}")
