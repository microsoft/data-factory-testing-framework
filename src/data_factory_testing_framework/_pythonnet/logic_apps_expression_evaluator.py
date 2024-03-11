import json
from typing import Union

from DataFactoryTestingFrameworkEvaluator import (
    ExpressionEvaluator,  # this is the .NET class that we want to use in Python
)

from data_factory_testing_framework.state import PipelineRunState


class LogicAppsExpressionEvaluator:
    @staticmethod
    def evaluate(expression: str, state: PipelineRunState) -> Union[str, int, float, bool, dict, list]:
        evaluator = ExpressionEvaluator()

        parameters = {parameter.type + parameter.name: parameter.value for parameter in state.parameters}
        variables = {variable.name: variable.value for variable in state.variables}

        expression = expression.replace("@pipeline().parameters.parameter", "@parameters('parametersparameter')")
        result = evaluator.EvaluateExpression(
            expression, json.dumps(parameters), json.dumps(variables), json.dumps(state.iteration_item)
        )
        return json.loads(result)["result"]
