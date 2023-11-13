class ExpressionParameterNotFoundError(Exception):
    def __init__(self, parameter_name: str) -> None:
        super().__init__(f"Parameter '{parameter_name}' not found")
