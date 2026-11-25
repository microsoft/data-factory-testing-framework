import re
from typing import List

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
from data_factory_testing_framework.mock import ExpressionMock
from data_factory_testing_framework.mock_context import MockContext
from data_factory_testing_framework.state import PipelineRunState, RunParameterType


class ExpressionRuntime:
    def __init__(self) -> None:
        """Initializes the expression runtime to transform and evaluate the expressions."""
        self.dftf_expressions_transformer = DataFactoryTestingFrameworkExpressionsTransformer()
        self.dftf_expressions_evaluator = DataFactoryTestingFrameworkExpressionsEvaluator()

    def _build_mock_config(
        self,
        mocks: List[ExpressionMock],
        mock_context: MockContext,
    ) -> dict:
        """Builds a mock configuration dictionary from the provided mocks and context."""
        mock_config = {}

        for mock in mocks:
            if mock.scope.is_in_scope(mock_context):
                # If we already have a mock for this function, we throw an error
                if mock.function_name in mock_config:
                    raise ValueError(
                        f'Duplicate mock function name detected: "{mock.function_name}". '
                        "Please ensure mocks have mutually exclusive scopes."
                    )
                else:
                    mock_config[mock.function_name] = mock.mock_result

        return mock_config

    def evaluate(
        self,
        expression: str,
        state: PipelineRunState,
        mocks: List[ExpressionMock],
        mock_context: MockContext,
    ) -> str:
        """Evaluate an expression with optional mocks and context."""
        mock_config = self._build_mock_config(mocks, mock_context)
        dftf_transformed_expression = self.dftf_expressions_transformer.transform_to_dftf_evaluator_expression(
            expression, state
        )
        try:
            result = self.dftf_expressions_evaluator.evaluate(dftf_transformed_expression, state, mock_config)
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

                if (
                    f"pipeline().parameters.{property_name}" in expression
                    and not state._contains_parameter_with_type_and_name(RunParameterType.Pipeline, property_name)
                ):
                    raise ParameterNotFoundError(RunParameterType.Pipeline, property_name) from e
                elif (
                    f"pipeline().globalParameters.{property_name}" in expression
                    and not state._contains_parameter_with_type_and_name(RunParameterType.Global, property_name)
                ):
                    raise ParameterNotFoundError(RunParameterType.Global, property_name) from e
                elif (
                    f"pipeline().libraryVariables.{property_name}" in expression
                    and not state._contains_parameter_with_type_and_name(
                        RunParameterType.LibraryVariables, property_name
                    )
                ):
                    raise ParameterNotFoundError(RunParameterType.LibraryVariables, property_name) from e
                elif (
                    f"pipeline().dataset.{property_name}" in expression
                    and not state._contains_parameter_with_type_and_name(RunParameterType.Dataset, property_name)
                ):
                    raise ParameterNotFoundError(RunParameterType.Dataset, property_name) from e
                elif (
                    f"pipeline().linkedService.{property_name}" in expression
                    and not state._contains_parameter_with_type_and_name(RunParameterType.LinkedService, property_name)
                ):
                    raise ParameterNotFoundError(RunParameterType.LinkedService, property_name) from e
                elif not state._contains_parameter_with_type_and_name(RunParameterType.System, property_name):
                    raise ParameterNotFoundError(RunParameterType.System, property_name) from e
                else:
                    raise Exception(
                        f"Unknown error for expression: '{expression}' with property: '{property_name}'. Internal error: '{e}'"
                    ) from e

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
