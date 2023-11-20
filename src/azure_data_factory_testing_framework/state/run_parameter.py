from typing import Generic, TypeVar

from azure_data_factory_testing_framework.state.run_parameter_type import RunParameterType

T = TypeVar("T")


class RunParameter(Generic[T]):
    def __init__(self, parameter_type: RunParameterType, name: str, value: T) -> None:
        """Run parameter. Represents a parameter that is being tracked during a pipeline run.

        Args:
            parameter_type: Type of the parameter.
            name: Name of the parameter.
            value: Value of the parameter.
        """
        self.type = parameter_type
        self.name = name
        self.value = value
