from abc import ABC, abstractmethod

from azure_data_factory_testing_framework.models.pipeline import Pipeline
from azure_data_factory_testing_framework.repositories.data_factory_repository import DataFactoryRepository


class BaseRepositoryFactory(ABC):
    def parse_from_folder(self, folder_path: str) -> DataFactoryRepository:
        pipelines = self._get_data_factory_pipelines_by_folder_path(folder_path)
        return DataFactoryRepository(pipelines)

    @abstractmethod
    def _get_data_factory_pipelines_by_folder_path(self, folder_path: str) -> list[Pipeline]:
        pass
