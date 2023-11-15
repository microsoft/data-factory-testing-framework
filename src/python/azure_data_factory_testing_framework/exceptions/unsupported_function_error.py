class UnsupportedFunctionError(Exception):
    def __init__(self, function_name: str) -> None:
        """Error raised when a function is not supported."""
        super().__init__(f"Unsupported function: {function_name}")
