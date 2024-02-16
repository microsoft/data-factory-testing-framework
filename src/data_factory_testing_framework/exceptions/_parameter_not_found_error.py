from data_factory_testing_framework.exceptions._user_error import UserError


class ParameterNotFoundError(UserError):
    def __init__(self, pipeline_type: str, name: str) -> None:
        """Error raised when a parameter is not found."""
        super().__init__(f"Parameter: '{name}' of type '{pipeline_type}' not found")
