from typing import List, Union

from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition


class ActivityDependency:
    """Activity dependency information.

    All required parameters must be populated in order to send to Azure.

    :ivar additional_properties: Unmatched properties from the message are deserialized to this
     collection.
    :vartype additional_properties: dict[str, JSON]
    :ivar activity: Activity name. Required.
    :vartype activity: str
    :ivar dependency_conditions: Match-Condition for the dependency. Required.
    :vartype dependency_conditions: list[str or ~azure.mgmt.datafactory.models.DependencyCondition]
    """

    def __init__(self, *, activity: str, dependency_conditions: List[Union[str, DependencyCondition]]) -> None:
        """ActivityDependency."""
        self.activity = activity
        self.dependency_conditions = dependency_conditions
