class PipelineNotFoundError(Exception):
    def __init__(self, pipeline_name: str) -> None:
        """Error raised when a pipeline is not found."""
        super().__init__(f"Pipeline with name {pipeline_name} not found")
