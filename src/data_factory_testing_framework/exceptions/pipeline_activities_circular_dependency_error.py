class NoRemainingPipelineActivitiesMeetDependencyConditionsError(Exception):
    """NoRemainingPipelineActivitiesMeetDependencyConditionsError.

    This error is raised when there are still pending pipeline activities, but no conditions are met to execute these activities.
    Scenarios where this error can be raised:
    * Circular dependencies in pipeline activities
    * Misconfigured pipeline activities
    """

    def __init__(self) -> None:
        """Initialize NoRemainingPipelineActivitiesMeetDependencyConditionsError."""
        super().__init__("No remaining pipeline activities meet dependency conditions.")
