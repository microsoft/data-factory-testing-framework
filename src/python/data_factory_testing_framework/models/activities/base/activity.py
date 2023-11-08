from typing import Any, List
from data_factory_testing_framework.generated.models import Activity, DependencyCondition, DataFactoryElement


class Activity:

    @staticmethod
    def patch_generated_models(models):
        models.Activity._evaluate_expressions = Activity.evaluate_expressions
        models.Activity.evaluate = Activity.evaluate
        models.Activity.status = None

    def evaluate(self: Activity):
        self._evaluate_expressions(self)
        self.status = DependencyCondition.Succeeded
        return self.status


    def evaluate_expressions(self, obj: Any, visited: List[Any] = None):
        if visited is None:
            visited = []

        if obj in visited:
            return

        visited.append(obj)

        attribute_names = [attribute for attribute in dir(obj) if not attribute.startswith('__') and not callable(getattr(obj, attribute))]
        for attributeName in attribute_names:
            attribute = getattr(obj, attributeName)
            if data_factory_element := isinstance(attribute, DataFactoryElement) and attribute:
                data_factory_element.evaluate()
            else:
                self._evaluate_expressions(attribute, visited)
