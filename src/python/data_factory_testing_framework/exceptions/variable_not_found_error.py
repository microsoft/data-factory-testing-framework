class VariableNotFoundError(Exception):
    def __init__(self, variable_name: str):
        super().__init__(f"Variable '{variable_name}' not found")