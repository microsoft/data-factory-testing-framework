from data_factory_testing_framework.exceptions._user_error import UserError


class ActivityNotFoundError(UserError):
    def __init__(self, activity_name: str) -> None:
        """Error raised when an activity is not found."""
        super().__init__(f"Activity with name '{activity_name}' not found")
