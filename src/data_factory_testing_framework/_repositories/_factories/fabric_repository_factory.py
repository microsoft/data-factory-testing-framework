import codecs
import os
from typing import List

from data_factory_testing_framework._deserializers._deserializer_fabric import (
    parse_fabric_pipeline_from_pipeline_json_files,
)
from data_factory_testing_framework._repositories._factories.base_repository_factory import BaseRepositoryFactory
from data_factory_testing_framework.models import Pipeline


class FabricRepositoryFactory(BaseRepositoryFactory):
    def _get_data_factory_pipelines_by_folder_path(self, folder_path: str) -> list[Pipeline]:
        pipeline_folders = FabricRepositoryFactory._find_folders_containing_pipeline(folder_path)
        pipelines = []
        for pipeline_folder in pipeline_folders:
            pipeline_file = os.path.join(pipeline_folder, "pipeline-content.json")
            pipeline_metadata_file = os.path.join(pipeline_folder, "item.metadata.json")
            pipeline_content_encoding = FabricRepositoryFactory._detect_encoding(pipeline_file)
            with open(pipeline_file, "r", encoding=pipeline_content_encoding) as pipeline_file, open(
                pipeline_metadata_file, "r"
            ) as pipeline_metadata_file:
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

    @staticmethod
    def _detect_encoding(file_path: str) -> str:
        """Detects the encoding of the file and returns it as a string.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The encoding of the file. Possible values are "utf-8" and "utf-16" (little or big endian).
        """
        with open(file_path, "rb") as file:
            bom = file.read(2)
            if bom == codecs.BOM_UTF16_LE or bom == codecs.BOM_UTF16_BE:
                return "utf-16"
            else:
                return "utf-8"
