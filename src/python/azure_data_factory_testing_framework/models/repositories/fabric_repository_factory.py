import os
from typing import List

from azure_data_factory_testing_framework.fabric_deserializer import parse_pipeline_from_json
from azure_data_factory_testing_framework.models.repositories.data_factory_repository import DataFactoryRepository


class FabricRepositoryFactory:
    @staticmethod
    def parse_from_folder(folder_path: str) -> DataFactoryRepository:
        pipelines = FabricRepositoryFactory._get_data_factory_pipelines_by_folder_path(folder_path)
        return DataFactoryRepository(pipelines)

    @staticmethod
    def _get_data_factory_pipelines_by_folder_path(folder_path: str) -> list:
        pipeline_files = FabricRepositoryFactory._find_files_with_name_in_folder("pipeline-content.json", folder_path)
        pipelines = []
        for pipeline_file in pipeline_files:
            with open(pipeline_file, "r") as f:
                pipelines.append(parse_pipeline_from_json(f.read()))

        return pipelines

    @staticmethod
    def _find_files_with_name_in_folder(filename: str, search_path: str) -> List[str]:
        result = []

        # Walk through the directory tree
        for root, _, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))

        return result
