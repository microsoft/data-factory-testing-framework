from typing import Any, Optional

from data_factory_testing_framework.state._dependency_condition import DependencyCondition


class ActivityResult:
    def __init__(self, activity_name: str, status: DependencyCondition, output: Optional[Any] = None) -> None:  # noqa: ANN401
        """Represents the result of an activity.

        Args:
            activity_name: Name of the activity.
            status: Status of the activity.
            output: Output of the activity. (e.g. { "count": 1 } for activity('activityName').output.count)
        """
        self.activity_name = activity_name
        self.status = status
        self.output = output

    def __getitem__(self, item: str) -> Any:  # noqa: ANN401
        return getattr(self, item)
