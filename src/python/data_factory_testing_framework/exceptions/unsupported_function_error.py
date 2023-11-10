class UnsupportedFunctionError(Exception):
    def __init__(self, function_name: str):
        super().__init__(f"Unsupported function: {function_name}")
