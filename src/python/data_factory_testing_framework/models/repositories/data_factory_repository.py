from typing import List

from data_factory_testing_framework.exceptions.pipeline_not_found_error import PipelineNotFoundError
from data_factory_testing_framework.generated.models import PipelineResource


class DataFactoryRepository:
    def __init__(self, pipelines: List[PipelineResource]) -> None:
        """Data factory repository.

        The data factory repository contains all the pipelines that can be evaluated.
        """
        self.pipelines = pipelines

    def get_pipeline_by_name(self, name: str) -> PipelineResource:
        for pipeline in self.pipelines:
            if pipeline.name == name:
                return pipeline

        raise PipelineNotFoundError(f"Pipeline with name {name} not found")
