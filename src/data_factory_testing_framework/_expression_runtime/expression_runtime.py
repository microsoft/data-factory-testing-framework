import re

from data_factory_testing_framework._expression_runtime.data_factory_expression.expression_transformer import (
    ExpressionTransformer as DataFactoryExpressionTransformer,
)
from data_factory_testing_framework._pythonnet.dotnet_expression_evaluator import DotnetExpressionEvaluator
from data_factory_testing_framework.exceptions import (
    ActivityNotFoundError,
    ParameterNotFoundError,
    StateIterationItemNotSetError,
    VariableNotFoundError,
)
from data_factory_testing_framework.state import PipelineRunState, RunParameterType


class ExpressionRuntime:
    def __init__(self) -> None:
        """Initializes the expression runtime."""
        self.data_factory_expression_transformer = DataFactoryExpressionTransformer()
        self.dotnet_expression_evaluator = DotnetExpressionEvaluator()

    def evaluate(self, expression: str, state: PipelineRunState) -> str:
        dotnet_evaluator_expression = self.data_factory_expression_transformer.transform_to_dotnet_evaluator_expression(
            expression, state
        )
        try:
            result = self.dotnet_expression_evaluator.evaluate(dotnet_evaluator_expression, state)
        except Exception as e:
            # match the exception type (coming from .NET) to the one we expect
            missing_parameter_match = re.match(
                r"(The template language expression \')(.*)(\' cannot be evaluated because property \')(.*)\' doesn't exist, available properties are .*",
                str(e),
            )

            missing_variable_match = re.match(
                r"(Template language expression cannot be evaluated: the template variable \')(.*)(\' cannot be found\.)",
                str(e),
            )

            missing_activity_match = re.match(
                r"(Template language expression cannot be evaluated: the template action \')(.*)(\' is not defined at current scope\.)",
                str(e),
            )

            # The template function 'item' is not expected at this location.
            missing_item_match = re.match(
                r"(The template function \')(.*)(\' is not expected at this location\.)",
                str(e),
            )

            if missing_parameter_match:
                expression = missing_parameter_match.group(2)
                property_name = missing_parameter_match.group(4)

                if expression.startswith("pipeline().parameters"):
                    raise ParameterNotFoundError(RunParameterType.Pipeline, property_name) from e
                elif expression.startswith("pipeline().globalParameters"):
                    raise ParameterNotFoundError(RunParameterType.Global, property_name) from e
                elif expression.startswith("pipeline().dataset"):
                    raise ParameterNotFoundError(RunParameterType.Dataset, property_name) from e
                elif expression.startswith("pipeline().linkedService"):
                    raise ParameterNotFoundError(RunParameterType.LinkedService, property_name) from e
                else:
                    raise ParameterNotFoundError(RunParameterType.System, property_name) from e

            if missing_variable_match:
                variable_name = missing_variable_match.group(2)
                raise VariableNotFoundError(variable_name) from e

            if missing_activity_match:
                activity_name = missing_activity_match.group(2)
                raise ActivityNotFoundError(activity_name) from e

            if missing_item_match:
                raise StateIterationItemNotSetError() from e

            raise Exception(f"Unknown error: {e}") from e

        return result
