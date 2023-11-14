class VariableNotFoundError(Exception):
    def __init__(self, variable_name: str) -> None:
        """Error raised when a variable is not found."""
        super().__init__(f"Variable '{variable_name}' not found")
