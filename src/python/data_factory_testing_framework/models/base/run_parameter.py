from typing import Generic, TypeVar

from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType

T = TypeVar("T")


class RunParameter(Generic[T]):
    def __init__(self, parameter_type: RunParameterType, name: str, value: T) -> None:
        """Run parameter.

        Args:
            parameter_type: Type of the parameter.
            name: Name of the parameter.
            value: Value of the parameter.
        """
        self.type = parameter_type
        self.name = name
        self.value = value
