import inspect
from typing import Any, Callable, Optional

from lark import Discard, Token, Transformer, Tree
from lxml.etree import _Element

from data_factory_testing_framework.exceptions.expression_evaluation_error import (
    ExpressionEvaluationError,
)
from data_factory_testing_framework.exceptions.state_iteration_item_not_set_error import (
    StateIterationItemNotSetError,
)
from data_factory_testing_framework.functions.functions_repository import FunctionsRepository
from data_factory_testing_framework.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.state.run_parameter_type import RunParameterType


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

    def literal_interpolation(self, value: list[Token, str, int, float, bool]) -> str:
        result = ""
        for item in value:
            if type(item) not in [str, int, float, bool, None]:
                raise ExpressionEvaluationError("Literal interpolation only supports string, int, float, bool and None")

            result += str(item)

        return result

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

    def expression_pipeline_reference(self, values: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if len(values) != 2:
            raise ExpressionEvaluationError("Pipeline reference should have two values")

        if not (isinstance(values[0], Token) and values[0].type == "EXPRESSION_PIPELINE_PROPERTY"):
            raise ExpressionEvaluationError('Pipeline reference requires Token "EXPRESSION_PIPELINE_PROPERTY"')

        if not (isinstance(values[1], Token) and values[1].type == "EXPRESSION_PARAMETER_NAME"):
            raise ExpressionEvaluationError('Pipeline reference requires Token "EXPRESSION_PARAMETER_NAME"')

        parameter_name = values[1]
        parameter_type = self._parse_run_parameter_type(values[0])
        return self.state.get_parameter_by_type_and_name(
            parameter_type,
            parameter_name,
        )

    def expression_variable_reference(self, values: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if len(values) != 1:
            raise ExpressionEvaluationError("Variable reference should have one value")

        if not (isinstance(values[0], Token) and values[0].type == "EXPRESSION_VARIABLE_NAME"):
            raise ExpressionEvaluationError('Variable reference requires Token "EXPRESSION_VARIABLE_NAME"')

        variable_name = values[0].value
        variable_name = variable_name[1:-1]  # remove quotes

        variable = self.state.get_variable_by_name(variable_name)

        return variable.value

    def expression_dataset_reference(self, values: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        if len(values) != 1:
            raise ExpressionEvaluationError("Dataset reference should have one value")

        if not (isinstance(values[0], Token) and values[0].type == "EXPRESSION_PARAMETER_NAME"):
            raise ExpressionEvaluationError('Dataset reference requires Token "EXPRESSION_PARAMETER_NAME"')

        parameter_name = values[0].value

        return self.state.get_parameter_by_type_and_name(
            RunParameterType.Dataset,
            parameter_name,
        )

    def expression_linked_service_reference(
        self, values: list[Token, str, int, float, bool]
    ) -> [str, int, float, bool]:
        if len(values) != 1:
            raise ExpressionEvaluationError("Linked service reference should have one value")

        if not (isinstance(values[0], Token) and values[0].type == "EXPRESSION_PARAMETER_NAME"):
            raise ExpressionEvaluationError('Linked service reference requires Token "EXPRESSION_PARAMETER_NAME"')

        parameter_name = values[0].value

        return self.state.get_parameter_by_type_and_name(
            RunParameterType.LinkedService,
            parameter_name,
        )

    def expression_activity_reference(
        self, values: list[Tree, Token, str, int, float, bool]
    ) -> [str, int, float, bool]:
        if len(values) != 2:
            raise ExpressionEvaluationError("Activity reference should have two values")

        expression_activity_name = values[0]
        if not isinstance(expression_activity_name, Token):
            raise ExpressionEvaluationError("Activity reference requires Token")

        if not expression_activity_name.type == "EXPRESSION_ACTIVITY_NAME":
            raise ExpressionEvaluationError('Activity reference requires Token "EXPRESSION_ACTIVITY_NAME"')

        activity_name = expression_activity_name.value
        activity_name = activity_name[1:-1]  # remove quotes

        activity = self.state.get_activity_result_by_name(activity_name)

        return self._evaluate_expression_object_accessors(activity, [values[1]])

    def expression_item_reference(self, values: list[Tree, Token, str, int, float, bool]) -> [str, int, float, bool]:
        if len(values) != 0:
            raise ExpressionEvaluationError("Item reference should not have any values")

        item = self.state.iteration_item
        if item is None:
            raise StateIterationItemNotSetError()

        return item

    def expression_system_variable_reference(
        self, values: list[Token, str, int, float, bool]
    ) -> [str, int, float, bool]:
        if len(values) != 1:
            raise ExpressionEvaluationError("System variable reference should have one value")

        if not (isinstance(values[0], Token) and values[0].type == "EXPRESSION_SYSTEM_VARIABLE_NAME"):
            raise ExpressionEvaluationError(
                'System variable reference requires Token "EXPRESSION_SYSTEM_VARIABLE_NAME"'
            )

        system_variable_name: Token = values[0]
        system_variable = self.state.get_parameter_by_type_and_name(
            RunParameterType.System,
            system_variable_name,
        )

        return system_variable

    def expression_function_parameters(self, values: list[Token, str, int, float, bool]) -> list:
        if not all(type(value) in [str, int, float, bool, list, _Element] or value is None for value in values):
            raise ExpressionEvaluationError("Function parameters should be string, int, float, bool, list or _Element")
        return values

    def expression_parameter(self, values: list[Token, str, int, float, bool, list]) -> str:
        if len(values) != 1:
            raise ExpressionEvaluationError("Function parameter must have only one value")

        parameter = values[0]

        if type(parameter) not in [str, int, float, bool, list, _Element, None] and parameter is not None:
            raise ExpressionEvaluationError("Function parameters should be string, int, float, bool, list or _Element")
        return parameter

    def expression_evaluation(self, values: list[Token, str, int, float, bool, list]) -> [str, int, float, bool]:
        eval_value = values[0]

        remaining_fields = values[1:]
        return self._evaluate_expression_object_accessors(eval_value, remaining_fields)

    def expression_interpolation_evaluation(
        self, values: list[Token, str, int, float, bool, list]
    ) -> [str, int, float, bool]:
        if len(values) != 1:
            raise ExpressionEvaluationError("Interpolation evaluation should have one value")

        return values[0]

    def expression_array_indices(self, values: list[Token, str, int, float, bool]) -> Optional[list[Token]]:
        if values[0] is None:
            return Discard  # if there are no array indices, discard the value
        if not all(isinstance(value, Token) and value.type == "EXPRESSION_ARRAY_INDEX" for value in values):
            raise ExpressionEvaluationError('Array indices should be of type "EXPRESSION_ARRAY_INDEX"')
        return values

    def expression_function_call(self, values: list[Token, str, int, float, bool]) -> [str, int, float, bool]:
        fn = values[0]
        fn_parameters = values[1] if len(values) == 2 and values[1] is not None else []
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
        # TODO: implement automatic conversion of parameters based on type hints
        result = function(*pos_or_keyword_values, *var_positional_values)

        return result

    @staticmethod
    def _evaluate_expression_object_accessors(current_item: Any, expression_object_accessors: list[Tree]) -> Any:  # noqa: ANN401
        if not all(
            isinstance(expression_object_accessor, Tree)
            and isinstance(expression_object_accessor.data, Token)
            and expression_object_accessor.data.value == "expression_object_accessor"
            for expression_object_accessor in expression_object_accessors
        ):
            raise ExpressionEvaluationError('Fields should be of type "expression_object_accessor"')

        for expression_object_accessor in expression_object_accessors:
            for field_token in expression_object_accessor.children:
                if not isinstance(field_token, Token):
                    raise ExpressionEvaluationError('Fields should be of type "Token"')
                if field_token.type == "EXPRESSION_PARAMETER_NAME":
                    if field_token.value not in current_item:
                        raise ValueError(field_token.value)

                    current_item = current_item[field_token.value]
                elif field_token.type == "EXPRESSION_ARRAY_INDEX":
                    if not isinstance(current_item, list):
                        raise ExpressionEvaluationError("Array index can only be used on lists")

                    current_item = current_item[field_token.value]
                else:
                    raise ExpressionEvaluationError(
                        'Fields should be of type "EXPRESSION_PARAMETER_NAME" or "EXPRESSION_ARRAY_INDEX"'
                    )

        return current_item

    @staticmethod
    def _parse_run_parameter_type(run_parameter_type: str) -> RunParameterType:
        if run_parameter_type == "parameters":
            return RunParameterType.Pipeline
        elif run_parameter_type == "globalParameters":
            return RunParameterType.Global
        else:
            raise ValueError(f"Unsupported run parameter type: {run_parameter_type}")
