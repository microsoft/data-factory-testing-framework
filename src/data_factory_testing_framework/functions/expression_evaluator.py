from typing import Union

from lark import Lark, Token, Tree, UnexpectedCharacters
from lark.exceptions import VisitError

from data_factory_testing_framework.exceptions.expression_parsing_error import ExpressionParsingError
from data_factory_testing_framework.functions._expression_transformer import ExpressionTransformer
from data_factory_testing_framework.functions.functions_repository import FunctionsRepository
from data_factory_testing_framework.state.pipeline_run_state import PipelineRunState


class ExpressionEvaluator:
    def __init__(self) -> None:
        """Evaluator for the expression language."""
        literal_grammar = """

            // literal rules
            ?literal_start: literal_evaluation
            literal_evaluation:  LITERAL_INT
                               | LITERAL_LETTER
                               | LITERAL_SINGLE_QUOTED_STRING
                               | LITERAL_BOOLEAN
                               | LITERAL_FLOAT
                               | LITERAL_NULL
                               | literal_array
            literal_array: "[" literal_evaluation ("," literal_evaluation)* "]"
            literal_interpolation: (LITERAL_LETTER* "@{" expression_evaluation "}" LITERAL_LETTER*)*


            // literal terminals:
            LITERAL_LETTER: /[^@]+/
            LITERAL_INT: SIGNED_INT
            LITERAL_FLOAT: SIGNED_FLOAT
            LITERAL_SINGLE_QUOTED_STRING: SINGLE_QUOTED_STRING
            LITERAL_BOOLEAN: BOOLEAN
            LITERAL_NULL: NULL
        """

        expression_grammar = f"""
            // TODO: add support for array index
            ?expression_start: expression_evaluation
            expression_evaluation: expression_call [expression_object_accessor]*
            ?expression_call: expression_function_call
                                    | expression_pipeline_reference
                                    | expression_variable_reference
                                    | expression_activity_reference
                                    | expression_dataset_reference
                                    | expression_linked_service_reference
                                    | expression_item_reference
                                    | expression_system_variable_reference
            expression_object_accessor: ["." EXPRESSION_PARAMETER_NAME] | [EXPRESSION_ARRAY_INDEX]

            // reference rules:
            expression_pipeline_reference: "pipeline" "()" "." EXPRESSION_PIPELINE_PROPERTY "." EXPRESSION_PARAMETER_NAME
            expression_variable_reference: "variables" "(" EXPRESSION_VARIABLE_NAME ")"
            expression_activity_reference: "activity" "(" EXPRESSION_ACTIVITY_NAME ")" expression_object_accessor
            expression_dataset_reference: "dataset" "()" "." EXPRESSION_PARAMETER_NAME
            expression_linked_service_reference: "linkedService" "()" "." EXPRESSION_PARAMETER_NAME
            expression_item_reference: "item" "()"
            expression_system_variable_reference: "pipeline" "()" "." EXPRESSION_SYSTEM_VARIABLE_NAME

            // function call rules
            expression_function_call: EXPRESSION_FUNCTION_NAME  "(" [expression_function_parameters] ")"
            expression_function_parameters: expression_parameter ("," expression_parameter )*
            expression_parameter: EXPRESSION_WS* (EXPRESSION_NULL | EXPRESSION_INTEGER | EXPRESSION_FLOAT | EXPRESSION_BOOLEAN | EXPRESSION_STRING | expression_start) EXPRESSION_WS*

            // expression terminals
            // EXPRESSION_PIPELINE_PROPERTY requires higher priority, because it clashes with pipeline().system_variable.field in the rule: expression_pipeline_reference
            EXPRESSION_PIPELINE_PROPERTY.2: "parameters" | "globalParameters"
            EXPRESSION_PARAMETER_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_VARIABLE_NAME: "'" /[^']*/ "'"
            EXPRESSION_ACTIVITY_NAME: "'" /[^']*/ "'"
            EXPRESSION_SYSTEM_VARIABLE_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_FUNCTION_NAME: {self._supported_functions()}
            EXPRESSION_NULL: NULL
            EXPRESSION_STRING: SINGLE_QUOTED_STRING
            EXPRESSION_INTEGER: SIGNED_INT
            EXPRESSION_FLOAT: SIGNED_FLOAT
            EXPRESSION_BOOLEAN: BOOLEAN
            EXPRESSION_WS: WS
            EXPRESSION_ARRAY_INDEX: ARRAY_INDEX
        """  # noqa: E501

        base_grammar = """
            ?start: ("@" expression_start) | (["@@"] literal_start) | (literal_interpolation)

            // shared custom basic data type rules:
            ARRAY_INDEX: "[" /[0-9]+/ "]"
            NULL: "null"
            BOOLEAN: "true" | "false"
            SINGLE_QUOTED_STRING: "'" /([^']|'')*/ "'"

            // imported lark terminals:
            %import common.SIGNED_INT
            %import common.SIGNED_FLOAT
            %import common.INT
            %import common.WS
        """

        grammer = base_grammar + literal_grammar + expression_grammar
        self.lark_parser = Lark(grammer, start="start", maybe_placeholders=False)

    def _supported_functions(self) -> str:
        functions = list(FunctionsRepository.functions.keys())
        functions = [f'"{f}"' for f in functions]
        return " | ".join(functions)

    def parse(self, expression: str) -> Tree[Token]:
        tree = self.lark_parser.parse(expression)
        return tree

    def evaluate(self, expression: str, state: PipelineRunState) -> Union[str, int, float, bool]:
        try:
            tree = self.parse(expression)
        except UnexpectedCharacters as uc:
            msg = f"""
            Expression could not be parsed.

            expression: {expression}
            line: {uc.line}
            column: {uc.column}
            char: {uc.char}
            """
            raise ExpressionParsingError(msg) from uc

        transformer = ExpressionTransformer(state)
        try:
            result: Tree = transformer.transform(tree)
        except VisitError as ve:
            raise ve.orig_exc from ve
        return result
