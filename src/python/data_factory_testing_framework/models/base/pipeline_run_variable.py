from typing import Generic, TypeVar

T = TypeVar("T")


class PipelineRunVariable(Generic[T]):
    def __init__(self, name: str, default_value: T = None):
        self.name = name
        self.value = default_value
