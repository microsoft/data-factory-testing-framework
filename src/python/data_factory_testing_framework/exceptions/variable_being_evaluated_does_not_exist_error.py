class VariableBeingEvaluatedDoesNotExistError(Exception):
    def __init__(self, variable_name) -> None:
        super().__init__(f"Variable being evaluated does not exist: {variable_name}")



