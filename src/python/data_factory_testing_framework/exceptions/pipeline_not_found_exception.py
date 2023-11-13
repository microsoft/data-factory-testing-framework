class PipelineNotFoundException(Exception):
    def __init__(self, pipeline_name) -> None:
        super().__init__(f"Pipeline with name {pipeline_name} not found")

