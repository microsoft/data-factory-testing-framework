from typing import TypeVar, Generic

T = TypeVar("T")


class RunVariable(Generic[T]):
    def __init__(self, name: str, default_value: T = None):
        self.name = name
        self.value = default_value
