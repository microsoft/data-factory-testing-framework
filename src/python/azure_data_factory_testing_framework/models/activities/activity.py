from typing import Any, List

from azure_data_factory_testing_framework.models.activities.activity_dependency import (
    ActivityDependency,
)
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.state import PipelineRunState
from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition


class Activity:
    def __init__(self, name: str, depends_on: List[ActivityDependency] = None, **kwargs: Any) -> None:  # noqa: ANN401
        """FabricActivity with dynamic dicts.

        Args:
            name: Name of the activity.
            depends_on: List of activities that this activity depends on.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if depends_on is None:
            depends_on = []

        self.name = name
        self.type = type
        self.depends_on = depends_on
        if "dependsOn" in kwargs:
            self.depends_on = []
            for dependency in kwargs["dependsOn"]:
                self.depends_on.append(
                    ActivityDependency(
                        activity=dependency["activity"], dependency_conditions=dependency["dependencyConditions"]
                    )
                )

        if "policy" in kwargs:
            self.policy: dict = kwargs["policy"]

        if "typeProperties" in kwargs:
            self.type_properties: dict = kwargs["typeProperties"]
        else:
            self.type_properties: dict = {}

        self.status: DependencyCondition = None

    def evaluate(self, state: PipelineRunState) -> "Activity":
        self._evaluate_expressions(self, state, types_to_ignore=[Activity])
        self.status = DependencyCondition.Succeeded
        return self

    def are_dependency_condition_met(self, state: PipelineRunState) -> bool:
        if not self.depends_on:
            return True

        for dependency in self.depends_on:
            dependency_activity = state.try_get_scoped_activity_result_by_name(dependency.activity)

            if dependency_activity is None:
                return False

            for dependency_condition in dependency.dependency_conditions:
                if dependency_activity["status"] != dependency_condition:
                    return False

        return True

    def _evaluate_expressions(
        self,
        obj: Any,  # noqa: ANN401
        state: PipelineRunState,
        visited: List[Any] = None,  # noqa: ANN401
        types_to_ignore: List[Any] = None,  # noqa: ANN401
    ) -> None:
        if visited is None:
            visited = []

        if obj in visited:
            return

        visited.append(obj)

        if data_factory_element := isinstance(obj, DataFactoryElement) and obj:
            data_factory_element.evaluate(state)
            return

        # Attributes
        attribute_names = [
            attribute
            for attribute in dir(obj)
            if not attribute.startswith("_") and not callable(getattr(obj, attribute))
        ]
        for attribute_name in attribute_names:
            attribute = getattr(obj, attribute_name)
            if attribute is None:
                continue

            self._evaluate_expressions(attribute, state, visited, types_to_ignore)

        # Dictionary
        if isinstance(obj, dict):
            for key in obj.keys():
                self._evaluate_expressions(obj[key], state, visited, types_to_ignore)

        # List
        if isinstance(obj, list):
            for item in obj:
                ignore_item = False
                for type_to_ignore in types_to_ignore:
                    if isinstance(item, type_to_ignore):
                        ignore_item = True

                if ignore_item:
                    continue

                self._evaluate_expressions(item, state, visited, types_to_ignore)
