from typing import Any, List

from data_factory_testing_framework.generated.models import Activity, DependencyCondition

from data_factory_testing_framework.models.repositories.data_factory_repository_factory import \
    DataFactoryRepositoryFactory


class TestFramework:

    def __init__(self, data_factory_folder_path: str):
        self.repository = DataFactoryRepositoryFactory.parse_from_folder(data_factory_folder_path)

    def evaluate(self, activity: Activity) -> DependencyCondition:
        return activity.evaluate()


