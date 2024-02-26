from lark import Lark, Token, Tree, UnexpectedCharacters

from data_factory_testing_framework._functions.evaluator.exceptions import (
    ExpressionEvaluationError,
    ExpressionParsingError,
)
from data_factory_testing_framework._functions.evaluator.expression_rule_transformer import (
    ExpressionRuleTransformer,
)
from data_factory_testing_framework._functions.evaluator.expression_terminal_transformer import (
    ExpressionTerminalTransformer,
)
from data_factory_testing_framework._functions.evaluator.rules import ExpressionRuleEvaluator
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult
from data_factory_testing_framework._functions.functions_repository import FunctionsRepository
from data_factory_testing_framework.models._data_factory_object_type import DataFactoryObjectType
from data_factory_testing_framework.state import PipelineRunState


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
            # TODO: probably object accessor does not apply to all below in expression_evaluation
            expression_evaluation: (expression_logical_bool | expression_branch | expression_call) ((("." EXPRESSION_PARAMETER_NAME) | EXPRESSION_ARRAY_INDEX)+)?
            ?expression_call: expression_function_call
                                    | expression_pipeline_reference
                                    | expression_variable_reference
                                    | expression_activity_reference
                                    | expression_dataset_reference
                                    | expression_linked_service_reference
                                    | expression_item_reference
                                    | expression_system_variable_reference

            // reference rules:
            expression_pipeline_reference: "pipeline" "()" "." EXPRESSION_PIPELINE_PROPERTY "." EXPRESSION_PARAMETER_NAME
            expression_variable_reference: "variables" "(" EXPRESSION_VARIABLE_NAME ")"
            expression_activity_reference: "activity" "(" EXPRESSION_ACTIVITY_NAME ")"
            expression_dataset_reference: "dataset" "()" "." EXPRESSION_PARAMETER_NAME
            expression_linked_service_reference: "linkedService" "()" "." EXPRESSION_PARAMETER_NAME
            expression_item_reference: "item" "()"
            expression_system_variable_reference: "pipeline" "()" "." EXPRESSION_SYSTEM_VARIABLE_NAME
            // branch rules
            expression_logical_bool: EXPRESSION_LOGICAL_BOOL "(" expression_parameter "," expression_parameter ")"
            expression_branch: "if" "(" expression_parameter "," expression_parameter "," expression_parameter ")"


            // function call rules
            expression_function_call: EXPRESSION_FUNCTION_NAME "(" [expression_parameter ("," expression_parameter )*] ")"
            ?expression_parameter: EXPRESSION_WS* (EXPRESSION_NULL | EXPRESSION_INTEGER | EXPRESSION_FLOAT | EXPRESSION_BOOLEAN | EXPRESSION_STRING | expression_start) EXPRESSION_WS*

            // expression terminals
            // EXPRESSION_PIPELINE_PROPERTY requires higher priority, because it clashes with pipeline().system_variable.field in the rule: expression_pipeline_reference
            EXPRESSION_ACTIVITY_NAME: "'" /[^']*/ "'"
            EXPRESSION_ARRAY_INDEX: ARRAY_INDEX
            EXPRESSION_BOOLEAN: BOOLEAN
            EXPRESSION_FLOAT: SIGNED_FLOAT
            EXPRESSION_FUNCTION_NAME: {self._supported_functions()}
            EXPRESSION_INTEGER: SIGNED_INT
            EXPRESSION_LOGICAL_BOOL: "or" | "and"
            EXPRESSION_NULL: NULL
            EXPRESSION_PARAMETER_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_PIPELINE_PROPERTY.2: "parameters" | "globalParameters"
            EXPRESSION_STRING: SINGLE_QUOTED_STRING
            EXPRESSION_SYSTEM_VARIABLE_NAME: /[a-zA-Z0-9_]+/
            EXPRESSION_VARIABLE_NAME: "'" /[^']*/ "'"
            EXPRESSION_WS: WS
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
        functions = list(FunctionsRepository._functions.keys())
        functions = [f'"{f}"' for f in functions]
        return " | ".join(functions)

    def _parse(self, expression: str) -> Tree[Token]:
        tree = self.lark_parser.parse(expression)
        return tree

    def evaluate(self, expression: str, state: PipelineRunState) -> DataFactoryObjectType:
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
        # we start with a raw parse tree for the lark grammer
        # and then semantically analysis it (in our case transforming values step by step)
        ast = parse_tree
        ast = ExpressionTerminalTransformer().transform(ast)
        ast = ExpressionRuleTransformer(state).transform(ast)
        if not isinstance(ast, ExpressionRuleEvaluator):
            raise ExpressionEvaluationError()
        result = ast.evaluate()
        if not isinstance(result, EvaluationResult):
            raise ExpressionEvaluationError()
        return result.value
