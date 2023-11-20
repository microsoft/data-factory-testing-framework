from typing import List, Union

from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition


class ActivityDependency:
    def __init__(self, activity: str, dependencyConditions: List[Union[str, DependencyCondition]] = None) -> None:  # noqa: ANN401, N803
        """ActivityDependency.

        Args:
            activity: Name of the activity.
            dependencyConditions: List of dependency conditions.
        """
        if dependencyConditions is None:
            dependencyConditions = []  # noqa: N806

        self.activity: str = activity
        self.dependency_conditions: List[DependencyCondition] = dependencyConditions
