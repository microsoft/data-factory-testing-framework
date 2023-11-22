import os
from typing import List

from azure_data_factory_testing_framework.deserializers._deserializer_fabric import (
    parse_fabric_pipeline_from_pipeline_json_files,
)
from azure_data_factory_testing_framework.models.pipeline import Pipeline
from azure_data_factory_testing_framework.repositories.base_repository_factory import BaseRepositoryFactory


class FabricRepositoryFactory(BaseRepositoryFactory):
    def _get_data_factory_pipelines_by_folder_path(self, folder_path: str) -> list[Pipeline]:
        pipeline_folders = FabricRepositoryFactory._find_folders_containing_pipeline(folder_path)
        pipelines = []
        for pipeline_folder in pipeline_folders:
            pipeline_file = os.path.join(pipeline_folder, "pipeline-content.json")
            pipeline_metadata_file = os.path.join(pipeline_folder, "item.metadata.json")
            with open(pipeline_file, "r") as pipeline_file, open(pipeline_metadata_file, "r") as pipeline_metadata_file:
                pipelines.append(
                    parse_fabric_pipeline_from_pipeline_json_files(pipeline_metadata_file.read(), pipeline_file.read())
                )

        return pipelines

    @staticmethod
    def _find_folders_containing_pipeline(search_path: str) -> List[str]:
        pipeline_folders = []

        # Walk through the directory tree and fine pipeline folders
        for root, _, files in os.walk(search_path):
            if "pipeline-content.json" in files:
                pipeline_folders.append(root)

        # Check if each folder contains metadata file
        for pipeline_folder in pipeline_folders:
            if "item.metadata.json" not in os.listdir(pipeline_folder):
                raise FileNotFoundError(f"Pipeline folder {pipeline_folder} does not contain metadata file")

        return pipeline_folders
