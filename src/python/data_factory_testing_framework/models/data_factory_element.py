from typing import Union

from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.generated.models import DataFactoryElement
from data_factory_testing_framework.models.state.run_state import RunState


class DataFactoryElement():
    def __init__(self) -> None:
        """DataFactoryElement."""
        self.value: Union[str, int, bool] = None

    def evaluate(self: DataFactoryElement, state: RunState) -> None:
        self.value = parse_expression(self.expression).evaluate(state)
        return self.value
