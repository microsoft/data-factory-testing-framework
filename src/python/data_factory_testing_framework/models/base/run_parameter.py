from typing import Generic, TypeVar

from data_factory_testing_framework.models.base.run_parameter_type import RunParameterType

T = TypeVar("T")


class RunParameter(Generic[T]):
    def __init__(self, type: RunParameterType, name: str, value: T) -> None:
        self.type = type
        self.name = name
        self.value = value
