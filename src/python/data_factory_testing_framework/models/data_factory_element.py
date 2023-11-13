from typing import Any, Generic, TypeVar

from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.generated.models import DataFactoryElement

T = TypeVar("T")


class DataFactoryElement(Generic[T]):
    def evaluate(self: DataFactoryElement, state: Any) -> None:  # noqa: ANN401
        self.value = parse_expression(self.expression).evaluate(state)
        return self.value
