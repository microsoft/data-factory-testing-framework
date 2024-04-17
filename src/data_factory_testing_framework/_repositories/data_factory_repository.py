from typing import List

from data_factory_testing_framework.exceptions import PipelineNotFoundError
from data_factory_testing_framework.models import Pipeline


class DataFactoryRepository:
    def __init__(self, pipelines: List[Pipeline]) -> None:
        """Initializes the repository with pipelines, linkedServices, datasets and triggers.

        Args:
            pipelines: List of pipelines.
        """
        self.pipelines = pipelines

    def get_pipeline_by_id(self, pipeline_id: str) -> Pipeline:
        """Get a pipeline by id. Throws an exception if the pipeline is not found.

        Args:
            pipeline_id: The identifier of the pipeline to get.

        Returns:
            The pipeline with the given id.
        """
        for pipeline in self.pipelines:
            if pipeline.pipeline_id == pipeline_id:
                return pipeline

        raise PipelineNotFoundError(f"Pipeline with pipeline_id: '{pipeline_id}' not found")

    def get_pipeline_by_name(self, name: str) -> Pipeline:
        """Get a pipeline by name. Throws an exception if the pipeline is not found.

        Args:
            name: Name of the pipeline.
        """
        for pipeline in self.pipelines:
            if pipeline.name == name:
                return pipeline

        raise PipelineNotFoundError(f"Pipeline with name: '{name}' not found")
