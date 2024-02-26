from data_factory_testing_framework.exceptions._user_error import UserError


class ActivityOutputFieldNotFoundError(UserError):
    def __init__(self, activity_name: str, output_field_name: str) -> None:
        """Exception raised when an activity does not have an expected output field."""
        super().__init__(
            f"Activity '{activity_name}' does not have output field '{output_field_name}'. Consider setting it through activity.setResult()."
        )
