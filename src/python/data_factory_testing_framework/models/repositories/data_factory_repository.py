from typing import List

from data_factory_testing_framework.exceptions.pipeline_not_found_error import PipelineNotFoundError
from data_factory_testing_framework.generated.models import PipelineResource


class DataFactoryRepository:
    def __init__(self, pipelines: List[PipelineResource]) -> None:
        """Initializes the repository with pipelines, linkedServices, datasets and triggers.

        Args:
            pipelines: List of pipelines.
        """
        self.pipelines = pipelines

    def get_pipeline_by_name(self, name: str) -> PipelineResource:
        """Get a pipeline by name. Throws an exception if the pipeline is not found.

        Args:
            name: Name of the pipeline.
        """
        for pipeline in self.pipelines:
            if pipeline.name == name:
                return pipeline

        raise PipelineNotFoundError(f"Pipeline with name {name} not found")
