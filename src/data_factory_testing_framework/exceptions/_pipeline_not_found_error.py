from data_factory_testing_framework.exceptions._user_error import UserError


class PipelineNotFoundError(UserError):
    def __init__(self, error_message: str) -> None:
        """Error raised when a pipeline is not found."""
        super().__init__(f"{error_message}")
