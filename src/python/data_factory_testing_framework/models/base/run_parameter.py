from typing import TypeVar, Generic

from data_factory_testing_framework.models.base.parameter_type import ParameterType

T = TypeVar("T")


class RunParameter(Generic[T]):
    def __init__(self, type: ParameterType, name: str, value: T):
        self.type = type
        self.name = name
        self.value = value
