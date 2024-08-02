import json
from typing import Union

# from System import Activator  # this is the .NET class that we want to use in Python
from Microsoft.Azure.DataFactoryTestingFramework.Expressions import (  # type: ignore
    Evaluator,  # this is the .NET class that we want to use in Python
)

from data_factory_testing_framework.state import PipelineRunState, RunParameterType


class DataFactoryTestingFrameworkExpressionsEvaluator:
    @staticmethod
    def evaluate(expression: str, state: PipelineRunState) -> Union[str, int, float, bool, dict, list]:
        evaluator = Evaluator()
        parameters = {
            "globalParameters": {},
            "parameters": {},
            "dataset": {},
            "linkedService": {},
        }

        for parameter in state.parameters:
            if parameter.type == RunParameterType.System:
                parameters[parameter.name] = parameter.value
            elif parameter.type == RunParameterType.Global:
                parameters["globalParameters"][parameter.name] = parameter.value
            elif parameter.type == RunParameterType.Pipeline:
                parameters["parameters"][parameter.name] = parameter.value
            elif parameter.type == RunParameterType.Dataset:
                parameters["dataset"][parameter.name] = parameter.value
            elif parameter.type == RunParameterType.LinkedService:
                parameters["linkedService"][parameter.name] = parameter.value

        activity_results = {}
        for activity in state.activity_results:
            activity_result_dir = {
                "outputs": {
                    "body": {
                        "output": activity.output,
                        "status": activity.status,
                    }
                }
            }
            activity_results[activity.activity_name] = activity_result_dir

        variables = {variable.name: variable.value for variable in state.variables}

        state_iter_item_json = json.dumps(state.iteration_item) if state.iteration_item else None

        result = evaluator.EvaluateExpression(
            expression,
            json.dumps(parameters),
            json.dumps(variables),
            state_iter_item_json,
            json.dumps(activity_results),
        )
        return json.loads(result)["result"]
