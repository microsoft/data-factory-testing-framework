from typing import Any, List

from azure_data_factory_testing_framework.generated.models import Activity, DataFactoryElement, DependencyCondition
from azure_data_factory_testing_framework.generated.models import Activity as GeneratedActivity
from azure_data_factory_testing_framework.state import PipelineRunState


class Activity:
    def evaluate(self, state: PipelineRunState) -> Activity:
        self.evaluate_expressions(self, state)
        self.status: DependencyCondition = DependencyCondition.Succeeded
        return self

    def evaluate_expressions(self, obj: Any, state: PipelineRunState, visited: List[Any] = None) -> None:  # noqa: ANN401
        if visited is None:
            visited = []

        if obj in visited:
            return

        visited.append(obj)

        if data_factory_element := isinstance(obj, DataFactoryElement) and obj:
            data_factory_element.evaluate(state)
            return

        attribute_names = [
            attribute
            for attribute in dir(obj)
            if not attribute.startswith("_") and not callable(getattr(obj, attribute))
        ]
        for attribute_name in attribute_names:
            attribute = getattr(obj, attribute_name)
            if attribute is None:
                continue

            if isinstance(attribute, dict):
                for key in attribute.keys():
                    self.evaluate_expressions(attribute[key], state, visited)
            elif isinstance(attribute, list):
                for item in attribute:
                    if isinstance(item, GeneratedActivity):
                        continue

                    self.evaluate_expressions(item, state, visited)
            else:
                self.evaluate_expressions(attribute, state, visited)

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
