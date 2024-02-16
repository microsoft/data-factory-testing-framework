from data_factory_testing_framework.exceptions._user_error import UserError


class VariableBeingEvaluatedDoesNotExistError(UserError):
    def __init__(self, variable_name: str) -> None:
        """Error raised when a variable being evaluated does not exist."""
        super().__init__(f"Variable being evaluated does not exist: {variable_name}")
