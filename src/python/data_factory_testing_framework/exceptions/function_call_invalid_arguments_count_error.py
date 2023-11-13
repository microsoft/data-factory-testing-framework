class FunctionCallInvalidArgumentsCountError(Exception):
    def __init__(self, name, evaluated_arguments, expected_argument_names) -> None:
        message = (
            f"FunctionCall {name} has invalid arguments count. "
            f"Evaluated arguments: \"{', '.join(map(str, evaluated_arguments))}\". "
            f"Expected argument types: {', '.join(expected_argument_names)}"
        )
        super().__init__(message)
