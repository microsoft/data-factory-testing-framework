class VariableBeingEvaluatedDoesNotExistError(Exception):
    def __init__(self, variable_name: str) -> None:
        """Error raised when a variable being evaluated does not exist."""
        super().__init__(f"Variable being evaluated does not exist: {variable_name}")
