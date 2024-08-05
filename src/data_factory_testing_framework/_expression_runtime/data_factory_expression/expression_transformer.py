from data_factory_testing_framework._expression_runtime.data_factory_expression.data_factory_to_expression_transformer import (
    DataFactoryExpressionTransformer,
)
from data_factory_testing_framework._expression_runtime.data_factory_expression.exceptions import (
    ExpressionParsingError,
)
from data_factory_testing_framework._expression_runtime.functions_repository import FunctionsRepository
from data_factory_testing_framework.models._data_factory_object_type import DataFactoryObjectType
from data_factory_testing_framework.state import PipelineRunState
from lark import Lark, Token, Tree, UnexpectedCharacters
from lark.reconstruct import Reconstructor


class ExpressionTransformer:
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
            expression_start: "@" expression_evaluation
            expression_evaluation: (expression_logical_bool | expression_branch | expression_call) ((("." EXPRESSION_PARAMETER_NAME) | EXPRESSION_ARRAY_INDEX)+)? EXPRESSION_WS*
            ?expression_call: expression_function_call
                              // used to translate to expression_pipeline_reference
                              | expression_datafactory_parameters_reference
                              | expression_pipeline_reference
                              // parse other language constructs
                              | expression_variable_reference
                              | expression_item_reference
                              | expression_datafactory_activity_reference

            // reference rules:
            expression_variable_reference: "variables" "(" EXPRESSION_VARIABLE_NAME ")"
            expression_datafactory_parameters_reference: EXPRESSION_DATAFACTORY_REFERENCE "()"
            expression_datafactory_activity_reference: "activity" "(" EXPRESSION_ACTIVITY_NAME ")"
            expression_item_reference: "item" "()"
            expression_pipeline_reference: "pipeline" "()" "." EXPRESSION_PIPELINE_PROPERTY



            // branch rules
            expression_logical_bool: EXPRESSION_LOGICAL_BOOL "(" expression_parameter "," expression_parameter ")"
            expression_branch: "if" "(" expression_parameter "," expression_parameter "," expression_parameter ")"


            // function call rules
            expression_function_call: EXPRESSION_FUNCTION_NAME "(" [expression_parameter ("," expression_parameter )*] ")"
            ?expression_parameter: EXPRESSION_WS* (EXPRESSION_NULL | EXPRESSION_INTEGER | EXPRESSION_FLOAT | EXPRESSION_BOOLEAN | EXPRESSION_STRING | expression_evaluation) EXPRESSION_WS*

            // expression terminals
            EXPRESSION_DATAFACTORY_REFERENCE: "dataset" | "linkedService"
            EXPRESSION_ACTIVITY_NAME: "'" /[^']*/ "'"
            EXPRESSION_ARRAY_INDEX: ARRAY_INDEX
            EXPRESSION_BOOLEAN: BOOLEAN
            EXPRESSION_FLOAT: SIGNED_FLOAT
            EXPRESSION_FUNCTION_NAME: {self._supported_functions()}
            EXPRESSION_INTEGER: SIGNED_INT
            EXPRESSION_LOGICAL_BOOL: "or" | "and"
            EXPRESSION_NULL: NULL
            EXPRESSION_PARAMETER_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_PIPELINE_PROPERTY: /[a-zA-Z0-9_]+/
            EXPRESSION_STRING: SINGLE_QUOTED_STRING
            EXPRESSION_SYSTEM_VARIABLE_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_VARIABLE_NAME: "'" /[^']*/ "'"
            EXPRESSION_WS: WS
        """  # noqa: E501

        base_grammar = """
            start: (expression_start) | (["@@"]+ literal_start) | (literal_interpolation)

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
        functions = [f'"{f}"' for f in FunctionsRepository._functions]
        return " | ".join(functions)

    def _parse(self, expression: str) -> Tree[Token]:
        tree = self.lark_parser.parse(expression)
        return tree

    def transform_to_dftf_evaluator_expression(self, expression: str, state: PipelineRunState) -> DataFactoryObjectType:
        try:
            parse_tree = self._parse(expression)

        except UnexpectedCharacters as uc:
            msg = f"""
            Expression could not be parsed.

            expression: {expression}
            line: {uc.line}
            column: {uc.column}
            char: {uc.char}
            """
            raise ExpressionParsingError(msg) from uc

        rule_transformer = DataFactoryExpressionTransformer()
        transformed_ast = rule_transformer.transform(parse_tree)
        expression_reconstructed = Reconstructor(self.lark_parser).reconstruct(transformed_ast)
        return expression_reconstructed
