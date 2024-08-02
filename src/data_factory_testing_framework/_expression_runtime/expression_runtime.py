import re

from data_factory_testing_framework._expression_runtime.data_factory_expression.expression_transformer import (
    ExpressionTransformer as DataFactoryTestingFrameworkExpressionsTransformer,
)
from data_factory_testing_framework._pythonnet.data_factory_testing_framework_expressions_evaluator import (
    DataFactoryTestingFrameworkExpressionsEvaluator,
)
from data_factory_testing_framework.exceptions import (
    ActivityNotFoundError,
    ParameterNotFoundError,
    StateIterationItemNotSetError,
    VariableNotFoundError,
)
from data_factory_testing_framework.state import PipelineRunState, RunParameterType


class ExpressionRuntime:
    def __init__(self) -> None:
        """Initializes the expression runtime to transform and evaluate the expressions."""
        self.dftf_expressions_transformer = DataFactoryTestingFrameworkExpressionsTransformer()
        self.dftf_expressions_evaluator = DataFactoryTestingFrameworkExpressionsEvaluator()

    def evaluate(self, expression: str, state: PipelineRunState) -> str:
        dftf_transformed_expression = self.dftf_expressions_transformer.transform_to_dftf_evaluator_expression(
            expression, state
        )
        try:
            result = self.dftf_expressions_evaluator.evaluate(dftf_transformed_expression, state)
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
