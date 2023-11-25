from typing import Union

from lark import Lark, Token, Tree
from lark.exceptions import VisitError

from azure_data_factory_testing_framework.functions._expression_transformer import ExpressionTransformer
from azure_data_factory_testing_framework.functions.functions_repository import FunctionsRepository
from azure_data_factory_testing_framework.state.pipeline_run_state import PipelineRunState


class ExpressionEvaluator:
    def __init__(self) -> None:
        """Evaluator for the expression language."""
        literal_grammer = """

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

            // literal terminals:
            LITERAL_LETTER: /[^@]+/
            LITERAL_INT: SIGNED_INT
            LITERAL_FLOAT: SIGNED_FLOAT
            LITERAL_SINGLE_QUOTED_STRING: SINGLE_QUOTED_STRING
            LITERAL_BOOLEAN: BOOLEAN
            LITERAL_NULL: NULL
        """

        expression_grammer = f"""
            // TODO: add support for array index
            ?expression_start: expression_evaluation
            expression_evaluation: expression_call [expression_array_indices]
            ?expression_call: expression_function_call 
                                    | expression_pipeline_reference
                                    | expression_variable_reference
                                    | expression_activity_reference
                                    | expression_dataset_reference
                                    | expression_linked_service_reference
                                    | expression_item_reference
            expression_array_indices: [EXPRESSION_ARRAY_INDEX]*

            // reference rules:
            expression_pipeline_reference: "pipeline" "()" "." EXPRESSION_PIPELINE_PROPERTY "." EXPRESSION_PARAMETER_NAME 
            expression_variable_reference: "variables" "(" EXPRESSION_VARIABLE_NAME ")"
            expression_activity_reference: "activity" "(" EXPRESSION_ACTIVITY_NAME ")" ("." EXPRESSION_PARAMETER_NAME)+
            expression_dataset_reference: "dataset" "(" EXPRESSION_DATASET_NAME ")"
            expression_linked_service_reference: "linkedService" "(" EXPRESSION_LINKED_SERVICE_NAME ")"
            expression_item_reference: "item()"

            // function call rules
            expression_function_call: EXPRESSION_FUNCTION_NAME  "(" expression_function_parameters ")"
            expression_function_parameters: expression_parameter ("," expression_parameter )*
            expression_parameter: EXPRESSION_WS* (EXPRESSION_NULL | EXPRESSION_INTEGER | EXPRESSION_FLOAT | EXPRESSION_BOOLEAN | EXPRESSION_STRING | expression_start) EXPRESSION_WS*
            
            // expression terminals
            EXPRESSION_PIPELINE_PROPERTY: "parameters" | "globalParameters"
            EXPRESSION_PARAMETER_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_VARIABLE_NAME: "'" /[^']*/ "'"
            EXPRESSION_ACTIVITY_NAME: "'" /[^']*/ "'"
            EXPRESSION_DATASET_NAME: "'" /[^']*/ "'"
            EXPRESSION_LINKED_SERVICE_NAME: "'" /[^']*/ "'"
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
            ?start: ("@" expression_start) | (["@@"] literal_start)
            
            // shared rules
            ARRAY_INDEX: "[" /[0-9]+/ "]"

            // shared custom basic data type rules:
            NULL: "null"
            BOOLEAN: "true" | "false"
            SINGLE_QUOTED_STRING: "'" /([^']|'')*/ "'"

            // imported lark terminals:
            %import common.SIGNED_INT
            %import common.SIGNED_FLOAT
            %import common.INT
            %import common.WS
        """

        grammer = base_grammar + literal_grammer + expression_grammer
        self.lark_parser = Lark(grammer, start="start")

    def _supported_functions(self) -> str:
        functions = list(FunctionsRepository.functions.keys())
        functions = [f'"{f}"' for f in functions]
        return " | ".join(functions)

    def parse(self, expression: str) -> Tree[Token]:
        tree = self.lark_parser.parse(expression)
        return tree

    def evaluate(self, expression: str, state: PipelineRunState) -> Union[str, int, float, bool]:
        tree: Tree = self.parse(expression)
        transformer = ExpressionTransformer(state)
        try:
            result: Tree = transformer.transform(tree)
        except VisitError as ve:
            raise ve.orig_exc from ve
        return result
