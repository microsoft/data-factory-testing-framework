import json
from typing import Union

from DataFactoryTestingFrameworkEvaluator import (
    ExpressionEvaluator,  # this is the .NET class that we want to use in Python
)

from data_factory_testing_framework.state import PipelineRunState


class DotnetExpressionEvaluator:
    def evaluate(self, expression: str, state: PipelineRunState) -> Union[str, int, float, bool]:
        evaluator = ExpressionEvaluator()

        # Set item Value From Json
        evaluator.SetItemValueFromJson(json.dumps(state.iteration_item))

        # Set variables from json
        parameters = {}
        for var in state.variables:
            parameters[var.name] = var.value
        evaluator.SetVariablesFromJson(json.dumps(parameters))

        result = evaluator.EvaluateExpression(expression)
        # Returns newton soft JValue
        return json.loads(result)["result"]


if __name__ == "__main__":
    result = DotnetExpressionEvaluator.evaluate()
    print(result)
