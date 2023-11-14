class ExpressionParameterNotFoundError(Exception):
    def __init__(self, parameter_name: str) -> None:
        """Error raised when an expression parameter is not found."""
        super().__init__(f"Parameter '{parameter_name}' not found")
