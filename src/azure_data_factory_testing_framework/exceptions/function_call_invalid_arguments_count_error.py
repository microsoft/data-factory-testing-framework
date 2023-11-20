class FunctionCallInvalidArgumentsCountError(Exception):
    def __init__(self, name: str, evaluated_arguments: list, expected_argument_names: list) -> None:
        """Error raised when a function call has an invalid arguments count."""
        message = (
            f"FunctionCall {name} has invalid arguments count. "
            f"Evaluated arguments: \"{', '.join(map(str, evaluated_arguments))}\". "
            f"Expected argument types: {', '.join(expected_argument_names)}"
        )
        super().__init__(message)
