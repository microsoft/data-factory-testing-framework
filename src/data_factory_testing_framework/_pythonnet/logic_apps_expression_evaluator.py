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

        parameters = {}
        # variables = {variable.name: variable.value for variable in state.variables}

        # expression = expression.replace("@pipeline().parameters.parameter", "@parameters('parametersparameter')")

        parameters = {
            "parameters": {parameter.name: parameter.value for parameter in state.parameters},
            "globalParameters": {
                global_parameter.name: global_parameter.value for global_parameter in state.parameters
            },
        }

        variables = {
            "pipeline": {
                # TODO: split parameters and globalParameters from state.parameters
                
            },
            "dataset": {parameter.name: parameter.value for parameter in state.parameters},
            "linkedService": {parameter.name: parameter.value for parameter in state.parameters},
        }



        for activity in state.activity_results:
            variables[f"activity_{activity.activity_name}"] = {"output": activity.output}

        for variable in state.variables:
            variables[f"v_{variable.name}"] = variable.value

        result = evaluator.EvaluateExpression(
            expression,
            json.dumps(parameters),
            json.dumps(variables),
            json.dumps(state.iteration_item),
        )
        return json.loads(result)["result"]
