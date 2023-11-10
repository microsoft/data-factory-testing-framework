from typing import Any, List
from data_factory_testing_framework.generated.models import Activity, DependencyCondition, DataFactoryElement
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class Activity:
    status: DependencyCondition

    def evaluate(self, state: PipelineRunState) -> Activity:
        self.evaluate_expressions(self, state)
        self.status = DependencyCondition.Succeeded
        return self

    def evaluate_expressions(self, obj: Any, state: PipelineRunState, visited: List[Any] = None):
        if visited is None:
            visited = []

        if obj in visited:
            return

        visited.append(obj)

        attribute_names = [attribute for attribute in dir(obj) if not attribute.startswith('__') and not callable(getattr(obj, attribute))]
        for attribute_name in attribute_names:
            attribute = getattr(obj, attribute_name)
            if data_factory_element := isinstance(attribute, DataFactoryElement) and attribute:
                data_factory_element.evaluate(state)
            else:
                self.evaluate_expressions(attribute, state, visited)

    def are_dependency_condition_met(self, state: PipelineRunState):
        if not self.depends_on:
            return True

        for dependency in self.depends_on:
            dependency_activity = state.get_scoped_activity_result_by_name(dependency.activity, state)

            if dependency_activity is None:
                return False

            for dependency_condition in dependency.dependency_conditions:
                if dependency_activity.status != dependency_condition:
                    return False

        return True


