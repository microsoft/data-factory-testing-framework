from typing import Any, List, Optional

from data_factory_testing_framework.models import DataFactoryElement
from data_factory_testing_framework.models.activities._activity_dependency import (
    ActivityDependency,
)
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


class Activity:
    def __init__(self, name: str, type: str, policy: Optional[dict] = None, **kwargs: Any) -> None:  # noqa: ANN401, A002
        """Activity with dynamic dicts.

        Args:
            name: Name of the activity.
            type: Type of the activity.
            policy: Policy of the activity.
            **kwargs: Activity properties coming directly from the json representation of the activity.
        """
        if policy is None:
            policy = {}

        self.name = name
        self.type = type
        self.policy = policy
        self.type_properties = kwargs["typeProperties"] if "typeProperties" in kwargs else {}

        self.depends_on: List[ActivityDependency] = []
        if "dependsOn" in kwargs:
            for dependency in kwargs["dependsOn"]:
                self.depends_on.append(ActivityDependency(**dependency))

        self.all_properties = kwargs

        self.status: DependencyCondition = None
        self.output = {}

    def evaluate(self, state: PipelineRunState) -> "Activity":
        self._evaluate_expressions(self, state, types_to_ignore=[Activity])
        self.status = DependencyCondition.Succeeded
        self.output = {}
        return self

    def are_dependency_condition_met(self, state: PipelineRunState) -> bool:
        if not self.depends_on:
            return True

        for dependency in self.depends_on:
            dependency_activity = state.try_get_activity_result_by_name(dependency.activity)

            if dependency_activity is None:
                return False

            for dependency_condition in dependency.dependency_conditions:
                if (
                    dependency_activity["status"] != dependency_condition
                    and dependency_condition != DependencyCondition.COMPLETED
                ):
                    return False

        return True

    def _evaluate_expressions(
        self,
        obj: Any,  # noqa: ANN401
        state: PipelineRunState,
        visited: Optional[List[Any]] = None,  # noqa: ANN401
        types_to_ignore: Optional[List[Any]] = None,  # noqa: ANN401
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
            if "activities" in attribute_name:
                continue

            attribute = getattr(obj, attribute_name)
            if attribute is None:
                continue

            self._evaluate_expressions(attribute, state, visited, types_to_ignore)

        # Dictionary
        if isinstance(obj, dict):
            for key in obj.keys():
                if "activities" in key:
                    continue

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

    def set_result(self, result: DependencyCondition, output: Optional[Any] = None) -> None:  # noqa: ANN401
        self.status = result
        self.output = output
