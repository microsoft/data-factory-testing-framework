class VariableDoesNotExistError(Exception):
    def __init__(self, variable_name: str) -> None:
        """Error raised when a variable does not exist."""
        super().__init__(f"Variable does not exist: {variable_name}")
