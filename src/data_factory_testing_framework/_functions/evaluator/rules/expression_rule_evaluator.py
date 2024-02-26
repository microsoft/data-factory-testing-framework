from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Union

from lark import Tree

from data_factory_testing_framework._functions.evaluator.exceptions import ExpressionEvaluationInvalidChildTypeError


@dataclass
class EvaluationResult:
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
        if not all(isinstance(child, (EvaluationResult, ExpressionRuleEvaluator)) for child in self.children):
            raise ExpressionEvaluationInvalidChildTypeError(
                expected_types=(EvaluationResult, ExpressionRuleEvaluator),
                actual_types=[type(child) for child in self.children],
            )

    @abstractmethod
    def evaluate(self) -> EvaluationResult:
        """Evaluates the expression rule."""
        pass

    @property
    def children(self) -> list[Union["ExpressionRuleEvaluator", EvaluationResult]]:
        """Returns the children of the expression rule."""
        return self._tree.children

    def evaluate_child(self, child: Union[EvaluationResult, "ExpressionRuleEvaluator"]) -> EvaluationResult:
        """Evaluates a child of the expression rule.

        If the child is an expression rule evaluator, it is evaluated so that the result is always an EvaluationResult.
        """
        if isinstance(child, ExpressionRuleEvaluator):
            return child.evaluate()
        else:
            return child
