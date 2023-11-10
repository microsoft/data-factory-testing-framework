from typing import Generic, TypeVar

T = TypeVar("T")


class DataFactoryElement(Generic[T]):
    expression: str
    value: T

    def __init__(self, expression: str):
        self.expression = expression

    def evaluate(self, state):
        return self.expression
