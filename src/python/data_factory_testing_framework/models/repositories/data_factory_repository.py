from typing import List

from data_factory_testing_framework.exceptions.pipeline_not_found_exception import PipelineNotFoundException
from data_factory_testing_framework.generated.models import PipelineResource


class DataFactoryRepository:
    def __init__(self, pipelines: List[PipelineResource]) -> None:
        self.pipelines = pipelines

    def get_pipeline_by_name(self, name: str) -> PipelineResource:
        for pipeline in self.pipelines:
            if pipeline.name == name:
                return pipeline

        raise PipelineNotFoundException(f"Pipeline with name {name} not found")
