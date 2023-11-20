import os

from azure_data_factory_testing_framework.deserializers.data_factory_deserializer import parse_pipeline_from_json
from azure_data_factory_testing_framework.repositories.data_factory_repository import (
    DataFactoryRepository,
)


class DataFactoryRepositoryFactory:
    @staticmethod
    def parse_from_folder(folder_path: str) -> DataFactoryRepository:
        pipeline_path = os.path.join(folder_path, "pipeline")
        pipelines = DataFactoryRepositoryFactory._get_data_factory_entities_by_folder_path(pipeline_path)
        return DataFactoryRepository(pipelines)

    @staticmethod
    def _get_data_factory_entities_by_folder_path(folder_path: str) -> list:
        pipelines = []
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if file.endswith(".json"):
                with open(file_path, "r") as f:
                    pipelines.append(parse_pipeline_from_json(f.read()))

        return pipelines
