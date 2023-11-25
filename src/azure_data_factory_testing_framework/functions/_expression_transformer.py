import inspect
from typing import Callable, Optional

from lark import Discard, Token, Transformer

from azure_data_factory_testing_framework.exceptions.activity_not_found_error import ActivityNotFoundError
from azure_data_factory_testing_framework.exceptions.dataset_parameter_not_found_error import (
    DatasetParameterNotFoundError,
)
from azure_data_factory_testing_framework.exceptions.expression_evaluation_error import (
    ExpressionEvaluationError,
)
from azure_data_factory_testing_framework.exceptions.expression_parameter_not_found_error import (
    ExpressionParameterNotFoundError,
)
from azure_data_factory_testing_framework.exceptions.linked_service_parameter_not_found_error import (
    LinkedServiceParameterNotFoundError,
)
from azure_data_factory_testing_framework.exceptions.state_iteration_item_not_set_error import (
    StateIterationItemNotSetError,
)
from azure_data_factory_testing_framework.exceptions.variable_not_found_error import VariableNotFoundError
from azure_data_factory_testing_framework.functions.functions_repository import FunctionsRepository
from azure_data_factory_testing_framework.state.pipeline_run_state import PipelineRunState
from azure_data_factory_testing_framework.state.run_parameter import RunParameter
from azure_data_factory_testing_framework.state.run_parameter_type import RunParameterType


class ExpressionTransformer(Transformer):
    def __init__(self, state: PipelineRunState) -> None:
        """Transformer for the Expression Language."""
        self.state: PipelineRunState = state
        super().__init__()

    def LITERAL_LETTER(self, token: Token) -> str:  # noqa: N802
        return str(token.value)

    def LITERAL_INT(self, token: Token) -> int:  # noqa: N802
        return int(token.value)

    def LITERAL_FLOAT(self, token: Token) -> float:  # noqa: N802
        return float(token.value)

    def LITERAL_SINGLE_QUOTED_STRING(self, token: Token) -> str:  # noqa: N802
        return str(token.value)

    def LITERAL_BOOLEAN(self, token: Token) -> bool:  # noqa: N802
        return bool(token.value)

    def LITERAL_NULL(self, token: Token) -> Optional[None]:  # noqa: N802
        return None

    def literal_evaluation(self, value: list[Token, str, int, float, bool]) -> [str, int, float, bool, None]:
        if len(value) != 1:
            raise ExpressionEvaluationError("Literal evaluation should have only one value")
        if type(value[0]) not in [str, int, float, bool, None]:
            raise ExpressionEvaluationError("Literal evaluation only supports string, int, float, bool and None")
        return value[0]

    def EXPRESSION_NULL(self, token: Token) -> Optional[None]:  # noqa: N802
        return None

    def EXPRESSION_STRING(self, token: Token) -> str:  # noqa: N802
        string = str(token.value)
        string = string.replace("''", "'")  # replace escaped single quotes
        string = string[1:-1]

        return string

    def EXPRESSION_INTEGER(self, token: Token) -> int:  # noqa: N802
        return int(token.value)

    def EXPRESSION_FLOAT(self, token: Token) -> float:  # noqa: N802
        return float(token.value)

    def EXPRESSION_BOOLEAN(self, token: Token) -> bool:  # noqa: N802
        return bool(token.value)

    def EXPRESSION_WS(self, token: Token) -> Discard:  # noqa: N802
        # Discard whitespaces in expressions
        return Discard

    def EXPRESSION_ARRAY_INDEX(self, token: Token) -> int:  # noqa: N802
        token.value = int(token.value[1:-1])
        return token

    def expression_pipeline_reference(self, value: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if not (isinstance(value[0], Token) and value[0].type == "EXPRESSION_PIPELINE_PROPERTY"):
            raise ExpressionEvaluationError('Pipeline reference requires Token "EXPRESSION_PIPELINE_PROPERTY"')

        if not (isinstance(value[1], Token) and value[1].type == "EXPRESSION_PARAMETER_NAME"):
            raise ExpressionEvaluationError('Pipeline reference requires Token "EXPRESSION_PARAMETER_NAME"')
        pipeline_reference_property: Token = value[0]
        pipeline_reference_property_parameter: Token = value[1]

        global_parameters: list[RunParameter] = list(
            filter(lambda p: p.type == RunParameterType.Global, self.state.parameters)
        )
        pipeline_parameters = list(filter(lambda p: p.type == RunParameterType.Pipeline, self.state.parameters))

        first = None
        if pipeline_reference_property == "parameters":
            first = list(filter(lambda p: p.name == pipeline_reference_property_parameter, pipeline_parameters))
        else:
            first = list(filter(lambda p: p.name == pipeline_reference_property_parameter, global_parameters))

        if len(first) == 0:
            raise ExpressionParameterNotFoundError(pipeline_reference_property_parameter)

        return first[0].value

    def expression_variable_reference(self, value: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if not (isinstance(value[0], Token) and value[0].type == "EXPRESSION_VARIABLE_NAME"):
            raise ExpressionEvaluationError('Variable reference requires Token "EXPRESSION_VARIABLE_NAME"')

        variable_name = value[0].value
        variable_name = variable_name[1:-1]  # remove quotes
        variable = list(filter(lambda p: p.name == variable_name, self.state.variables))

        if len(variable) == 0:
            raise VariableNotFoundError(variable_name)
        return variable[0].value

    def expression_dataset_reference(self, value: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if not (isinstance(value[0], Token) and value[0].type == "EXPRESSION_DATASET_NAME"):
            raise ExpressionEvaluationError('Dataset reference requires Token "EXPRESSION_DATASET_NAME"')

        dataset_name = value[0].value
        dataset_name = dataset_name[1:-1]  # remove quotes
        datasets = list(filter(lambda p: p.type == RunParameterType.Dataset, self.state.parameters))
        dataset = list(filter(lambda p: p.name == dataset_name, datasets))

        if len(dataset) == 0:
            raise DatasetParameterNotFoundError(dataset_name)
        return dataset[0].value

    def expression_linked_service_reference(self, value: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if not (isinstance(value[0], Token) and value[0].type == "EXPRESSION_LINKED_SERVICE_NAME"):
            raise ExpressionEvaluationError('Linked service reference requires Token "EXPRESSION_LINKED_SERVICE_NAME"')

        linked_service_name = value[0].value
        linked_service_name = linked_service_name[1:-1]  # remove quotes
        linked_services = list(filter(lambda p: p.type == RunParameterType.LinkedService, self.state.parameters))
        linked_service = list(filter(lambda p: p.name == linked_service_name, linked_services))

        if len(linked_service) == 0:
            raise LinkedServiceParameterNotFoundError(linked_service_name)
        return linked_service[0].value

    def expression_activity_reference(self, values: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if not (isinstance(values[0], Token) and values[0].type == "EXPRESSION_ACTIVITY_NAME"):
            raise ExpressionEvaluationError('Activity reference requires Token "EXPRESSION_ACTIVITY_NAME"')

        activity_name = values[0].value
        activity_name = activity_name[1:-1]  # remove quotes

        if not all(isinstance(value, Token) and value.type == "EXPRESSION_PARAMETER_NAME" for value in values[1:]):
            raise ExpressionEvaluationError(
                'Activity property and fields should be of type "EXPRESSION_PARAMETER_NAME"'
            )

        activity_property = values[1]
        property_fields = values[2:]

        activity = self.state.try_get_scoped_activity_result_by_name(activity_name)
        if activity is None:
            raise ActivityNotFoundError(activity_name)

        activity_property_parameter = activity[activity_property]
        for field in property_fields:
            field_value = field.value
            activity_property_parameter = activity_property_parameter[field_value]
        return activity_property_parameter

    def expression_item_reference(self, value: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        item = self.state.iteration_item
        if item is None:
            raise StateIterationItemNotSetError()
        return item

    def expression_function_parameters(self, values: list[Token, str, int, float, bool]) -> list:
        if not all(type(value) in [str, int, float, bool, list] for value in values):
            raise ExpressionEvaluationError("Function parameters should be string, int, float, bool or list")
        return values

    def expression_parameter(self, values: list[Token, str, int, float, bool, list]) -> str:
        if len(values) != 1:
            raise ExpressionEvaluationError("Function parameter must have only one value")
        parameter = values[0]
        if type(parameter) not in [str, int, float, bool, list]:
            raise ExpressionEvaluationError("Function parameters should be string, int, float, bool or list")
        return parameter

    def expression_evaluation(self, values: list[Token, str, int, float, bool, list]) -> [str, int, float, bool]:
        eval_value = values[0]
        if len(values) == 1:
            return eval_value

        if not all(
            isinstance(array_index, Token) or array_index.type == "EXPRESSION_ARRAY_INDEX" for array_index in values[1]
        ):
            raise ExpressionEvaluationError('Array indices should be of type "EXPRESSION_ARRAY_INDEX"')

        array_indices: list[Token] = values[1]
        for array_index in array_indices:
            eval_value = eval_value[array_index.value]
        return eval_value

    def expression_array_indices(self, values: list[Token, str, int, float, bool]) -> Optional[list[Token]]:
        if values[0] is None:
            return Discard  # if there are no array indices, discard the value
        if not all(isinstance(value, Token) and value.type == "EXPRESSION_ARRAY_INDEX" for value in values):
            raise ExpressionEvaluationError('Array indices should be of type "EXPRESSION_ARRAY_INDEX"')
        return values

    def expression_function_call(self, values: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        fn = values[0]
        fn_parameters = values[1]
        function: Callable = FunctionsRepository.functions.get(fn.value)

        pos_or_keyword_parameters = []

        function_signature = inspect.signature(function)
        pos_or_keyword_parameters = [
            param
            for param in function_signature.parameters.values()
            if param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ]

        pos_or_keyword_values = fn_parameters[: len(pos_or_keyword_parameters)]
        var_positional_values = fn_parameters[len(pos_or_keyword_parameters) :]  # should be 0 or 1

        result = function(*pos_or_keyword_values, *var_positional_values)
        return result
