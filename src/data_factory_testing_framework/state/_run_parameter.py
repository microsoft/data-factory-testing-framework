from data_factory_testing_framework.models._data_factory_object_type import DataFactoryObjectType
from data_factory_testing_framework.state._run_parameter_type import RunParameterType


class RunParameter:
    def __init__(self, parameter_type: RunParameterType, name: str, value: DataFactoryObjectType) -> None:
        """Run parameter. Represents a parameter that is being tracked during a pipeline run.

        Args:
            parameter_type: Type of the parameter.
            name: Name of the parameter.
            value: Value of the parameter.
        """
        self.type = parameter_type
        self.name = name
        self.value = value
