class ParameterNotFoundError(Exception):
    def __init__(self, pipeline_type: str, name: str) -> None:
        """Error raised when a parameter is not found."""
        super().__init__(f"Parameter: '{name}' of type '{pipeline_type}' not found")
