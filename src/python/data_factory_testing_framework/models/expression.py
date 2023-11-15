from typing import TypeVar, Any

from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.generated.models import Expression
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState

TResult = TypeVar("TResult")


class Expression:
    def __init__(self) -> None:
        """Expression."""
        self.evaluated: Any = None

    def evaluate(self: Expression, state: PipelineRunState) -> TResult:
        """Evaluates the expression by replacing all parameters and variables with their values and then evaluating the expression.

        Args:
            state: The state to use for evaluating the expression.
        """
        self.evaluated = parse_expression(self.value).evaluate(state)
        return self.evaluated
