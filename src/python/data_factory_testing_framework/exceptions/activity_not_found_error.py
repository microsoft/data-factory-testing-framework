class ActivityNotFoundError(Exception):
    def __init__(self, activity_name: str) -> None:
        """Error raised when an activity is not found."""
        super().__init__(f"Activity with name {activity_name} not found")
