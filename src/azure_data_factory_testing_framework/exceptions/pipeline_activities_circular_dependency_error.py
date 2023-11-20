class PipelineActivitiesCircularDependencyError(Exception):
    def __init__(self) -> None:
        """Exception for circular dependencies in pipeline activities."""
        super().__init__("Circular dependency detected in pipeline activities")
