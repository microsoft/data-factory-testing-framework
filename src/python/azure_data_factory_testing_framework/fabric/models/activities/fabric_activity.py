from typing import Any, List

from azure_data_factory_testing_framework.fabric.models.activities.fabric_activity_dependency import (
    FabricActivityDependency,
)
from azure_data_factory_testing_framework.fabric.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.state import PipelineRunState
from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition


class FabricActivity:
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """FabricActivity with dynamic dicts.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.name: str = kwargs["name"]
        self.type: str = kwargs["type"]
        self.depends_on: List[FabricActivityDependency] = kwargs["dependsOn"]
        if "policy" in kwargs:
            self.policy: dict = kwargs["policy"]

        self.type_properties: dict = kwargs["typeProperties"]
        self.status: DependencyCondition = None

    def evaluate(self, state: PipelineRunState) -> "FabricActivity":
        self._evaluate_expressions(self, state, types_to_ignore=[type("FabricActivity")])
        self.status = DependencyCondition.Succeeded
        return self

    def are_dependency_condition_met(self, state: PipelineRunState) -> bool:
        if not self.depends_on:
            return True

        for dependency in self.depends_on:
            dependency_activity = state.try_get_scoped_activity_result_by_name(dependency["activity"])

            if dependency_activity is None:
                return False

            for dependency_condition in dependency["dependencyConditions"]:
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
                for type_to_ignore in types_to_ignore:
                    if isinstance(item, type_to_ignore):
                        continue

                self._evaluate_expressions(item, state, visited, types_to_ignore)
