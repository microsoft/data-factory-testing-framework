class UnsupportedFunctionError(Exception):
    def __init__(self, function_name: str) -> None:
        super().__init__(f"Unsupported function: {function_name}")
