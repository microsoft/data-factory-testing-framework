from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union

from lark import Tree

from data_factory_testing_framework.functions.evaluator.exceptions import ExpressionEvaluationInvalidChildTypeError


@dataclass
class EvaluatedExpression:
    """Evaluated expression data class."""

    value: Any


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
        if not all(isinstance(child, (EvaluatedExpression, ExpressionRuleEvaluator)) for child in self.children):
            raise ExpressionEvaluationInvalidChildTypeError(
                expected_types=(EvaluatedExpression, ExpressionRuleEvaluator),
                actual_types=[type(child) for child in self.children],
            )

    @abstractmethod
    def evaluate(self) -> EvaluatedExpression:
        """Evaluates the expression rule."""
        pass

    @property
    def children(self) -> list[Union["ExpressionRuleEvaluator", EvaluatedExpression]]:
        """Returns the children of the expression rule."""
        return self._tree.children

    def ensure_evaluated_expression(
        self, child: Union[EvaluatedExpression, "ExpressionRuleEvaluator"]
    ) -> EvaluatedExpression:
        if isinstance(child, ExpressionRuleEvaluator):
            return child.evaluate()
        else:
            return child
