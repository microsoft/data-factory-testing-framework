import codecs
import json
import os
from typing import List

from data_factory_testing_framework._deserializers._deserializer_fabric import (
    parse_fabric_pipeline_from_pipeline_json_files,
)
from data_factory_testing_framework._repositories._factories.base_repository_factory import BaseRepositoryFactory
from data_factory_testing_framework.models import Pipeline

REQUIRED_FILES = ["pipeline-content.json", ".platform"]


class FabricRepositoryFactory(BaseRepositoryFactory):
    def _get_data_factory_pipelines_by_folder_path(self, folder_path: str) -> list[Pipeline]:
        pipeline_folders = FabricRepositoryFactory._find_folders_containing_pipeline(folder_path)
        pipelines = []
        for pipeline_folder in pipeline_folders:
            pipeline_file = os.path.join(pipeline_folder, "pipeline-content.json")
            pipeline_content_encoding = FabricRepositoryFactory._detect_encoding(pipeline_file)

            platform_file = os.path.join(pipeline_folder, ".platform")
            with open(pipeline_file, "r", encoding=pipeline_content_encoding) as pipeline_file, open(
                platform_file, "r"
            ) as platform_file:
                pipeline_contents = pipeline_file.read()
                platform_config: dict = json.load(platform_file)

                if not all(key in platform_config.keys() for key in ["metadata", "config"]):
                    raise ValueError(
                        f"Platform file {platform_file} does not contain the required keys metadata and config"
                    )

                pipelines.append(
                    parse_fabric_pipeline_from_pipeline_json_files(
                        pipeline_contents, platform_config["config"], platform_config["metadata"]
                    )
                )

        return pipelines

    @staticmethod
    def _find_folders_containing_pipeline(search_path: str) -> List[str]:
        pipeline_folders = []

        # Walk through the directory tree and find pipeline folders
        for root, _, files in os.walk(search_path):
            if "pipeline-content.json" in files:
                pipeline_folders.append(root)

        # Check if each folder contains the required files
        for pipeline_folder in pipeline_folders:
            list_dir = os.listdir(pipeline_folder)
            if not all(file in list_dir for file in REQUIRED_FILES):
                raise FileNotFoundError(
                    f"Pipeline folder {pipeline_folder} does not contain the required files {REQUIRED_FILES}"
                )

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
