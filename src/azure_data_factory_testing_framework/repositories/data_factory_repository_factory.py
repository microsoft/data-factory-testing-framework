import os

from azure_data_factory_testing_framework.deserializers._deserializer_data_factory import (
    parse_data_factory_pipeline_from_pipeline_json,
)
from azure_data_factory_testing_framework.models.pipeline import Pipeline
from azure_data_factory_testing_framework.repositories.base_repository_factory import BaseRepositoryFactory


class DataFactoryRepositoryFactory(BaseRepositoryFactory):
    def _get_data_factory_pipelines_by_folder_path(self, folder_path: str) -> list[Pipeline]:
        pipeline_path = os.path.join(folder_path, "pipeline")
        pipelines = []
        files = os.listdir(pipeline_path)
        for file in files:
            file_path = os.path.join(pipeline_path, file)
            if file.endswith(".json"):
                with open(file_path, "r") as f:
                    pipelines.append(parse_data_factory_pipeline_from_pipeline_json(f.read()))

        return pipelines
