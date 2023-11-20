from typing import Any, List, Union

from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition


class ActivityDependency:
    def __init__(self, **kwargs: Any) -> None: # noqa: ANN401
        """ActivityDependency.

        Args:
            **kwargs: ActivityDependency properties coming directly from the json representation of the activity.
        """
        self.kwargs = kwargs
        self.activity: str = kwargs["activity"]
        self.dependency_conditions: List[Union[str, DependencyCondition]] = kwargs["dependencyConditions"]
