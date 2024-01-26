# ruff: noqa: N802


from lark import Discard, Token, Transformer

from data_factory_testing_framework.exceptions.expression_evaluation_error import ExpressionEvaluationError
from data_factory_testing_framework.functions.evaluator.rules.expression_rule import EvaluatedExpression
from data_factory_testing_framework.state.run_parameter_type import RunParameterType


class ExpressionTerminalTransformer(Transformer):
    def EXPRESSION_ACTIVITY_NAME(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value[1:-1])

    def EXPRESSION_ARRAY_INDEX(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(int(token.value[1:-1]))

    def EXPRESSION_BOOLEAN(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(bool(token.value))

    def EXPRESSION_FLOAT(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(float(token.value))

    def EXPRESSION_FUNCTION_NAME(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value)

    def EXPRESSION_INTEGER(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(int(token.value))

    def EXPRESSION_LOGICAL_BOOL(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value)

    def EXPRESSION_NULL(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(None)

    def EXPRESSION_PARAMETER_NAME(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value)

    def EXPRESSION_PIPELINE_PROPERTY(self, token: Token) -> EvaluatedExpression:
        if token.value == "parameters":
            return EvaluatedExpression(RunParameterType.Pipeline)
        elif token.value == "globalParameters":
            return EvaluatedExpression(RunParameterType.Global)
        else:
            raise ExpressionEvaluationError(f"Unsupported run parameter type: {token.value}")

    def EXPRESSION_STRING(self, token: Token) -> EvaluatedExpression:
        string = str(token.value)
        string = string.replace("''", "'")  # replace escaped single quotes
        string = string[1:-1]

        return EvaluatedExpression(string)

    def EXPRESSION_SYSTEM_VARIABLE_NAME(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value)

    def EXPRESSION_VARIABLE_NAME(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value[1:-1])

    def EXPRESSION_WS(self, token: Token) -> Discard:
        # Discard whitespaces in expressions
        return Discard

    def LITERAL_LETTER(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(token.value)

    def LITERAL_INT(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(int(token.value))

    def LITERAL_FLOAT(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(float(token.value))

    def LITERAL_SINGLE_QUOTED_STRING(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(str(token.value))

    def LITERAL_BOOLEAN(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(bool(token.value))

    def LITERAL_NULL(self, token: Token) -> EvaluatedExpression:
        return EvaluatedExpression(None)
