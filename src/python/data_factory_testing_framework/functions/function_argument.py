class FunctionArgument:
    def __init__(self, expression: str):
        self.expression = expression.strip('\n').strip(' ')