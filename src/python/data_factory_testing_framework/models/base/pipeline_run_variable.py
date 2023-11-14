from typing import Generic, TypeVar

T = TypeVar("T")


class PipelineRunVariable(Generic[T]):
    def __init__(self, name: str, default_value: T = None) -> None:
        """Represents a pipeline variable that is being tracked during a pipeline run.

        Args:
            name: Name of the variable.
            default_value: Default value of the variable. Defaults to None.
        """
        self.name = name
        self.value = default_value
