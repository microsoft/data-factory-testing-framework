import json
from typing import Union

from DataFactoryTestingFrameworkEvaluator import (
    ExpressionEvaluator,  # this is the .NET class that we want to use in Python
)

from data_factory_testing_framework._functions.evaluator.expression_evaluator import ExpressionEvaluator
from data_factory_testing_framework.state import PipelineRunState


class DotnetExpressionEvaluator:
    def evaluate(self, expression: str, state: PipelineRunState) -> Union[str, int, float, bool, dict, list]:
        expression_state_populator = ExpressionEvaluator()
        expression = expression_state_populator.evaluate(expression, state)

        evaluator = ExpressionEvaluator()
        result = evaluator.EvaluateExpression(expression)
        # Returns newton soft JValue
        return json.loads(result)["result"]


if __name__ == "__main__":
    result = DotnetExpressionEvaluator.evaluate()
    print(result)
