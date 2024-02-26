from typing import Optional

from data_factory_testing_framework.models._data_factory_object_type import DataFactoryObjectType


class PipelineRunVariable:
    def __init__(self, name: str, default_value: Optional[DataFactoryObjectType] = None) -> None:
        """Represents a pipeline variable that is being tracked during a pipeline run.

        Args:
            name: Name of the variable.
            default_value: Default value of the variable. Defaults to None.
        """
        self.name = name
        self.value = default_value
