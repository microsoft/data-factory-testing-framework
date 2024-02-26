# ruff: noqa: N802


from lark import Discard, Token, Transformer

from data_factory_testing_framework._functions.evaluator.exceptions import ExpressionEvaluationError
from data_factory_testing_framework._functions.evaluator.rules.expression_rule_evaluator import EvaluationResult
from data_factory_testing_framework.state._run_parameter_type import RunParameterType


class ExpressionTerminalTransformer(Transformer):
    def EXPRESSION_ACTIVITY_NAME(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value[1:-1])

    def EXPRESSION_ARRAY_INDEX(self, token: Token) -> EvaluationResult:
        return EvaluationResult(int(token.value[1:-1]))

    def EXPRESSION_BOOLEAN(self, token: Token) -> EvaluationResult:
        return EvaluationResult(bool(token.value))

    def EXPRESSION_FLOAT(self, token: Token) -> EvaluationResult:
        return EvaluationResult(float(token.value))

    def EXPRESSION_FUNCTION_NAME(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value)

    def EXPRESSION_INTEGER(self, token: Token) -> EvaluationResult:
        return EvaluationResult(int(token.value))

    def EXPRESSION_LOGICAL_BOOL(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value)

    def EXPRESSION_NULL(self, token: Token) -> EvaluationResult:
        return EvaluationResult(None)

    def EXPRESSION_PARAMETER_NAME(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value)

    def EXPRESSION_PIPELINE_PROPERTY(self, token: Token) -> EvaluationResult:
        if token.value == "parameters":
            return EvaluationResult(RunParameterType.Pipeline)
        elif token.value == "globalParameters":
            return EvaluationResult(RunParameterType.Global)
        else:
            raise ExpressionEvaluationError(f"Unsupported run parameter type: {token.value}")

    def EXPRESSION_STRING(self, token: Token) -> EvaluationResult:
        string = str(token.value)
        string = string.replace("''", "'")  # replace escaped single quotes
        string = string[1:-1]

        return EvaluationResult(string)

    def EXPRESSION_SYSTEM_VARIABLE_NAME(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value)

    def EXPRESSION_VARIABLE_NAME(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value[1:-1])

    def EXPRESSION_WS(self, token: Token) -> Discard:
        # Discard whitespaces in expressions
        return Discard

    def LITERAL_LETTER(self, token: Token) -> EvaluationResult:
        return EvaluationResult(token.value)

    def LITERAL_INT(self, token: Token) -> EvaluationResult:
        return EvaluationResult(int(token.value))

    def LITERAL_FLOAT(self, token: Token) -> EvaluationResult:
        return EvaluationResult(float(token.value))

    def LITERAL_SINGLE_QUOTED_STRING(self, token: Token) -> EvaluationResult:
        return EvaluationResult(str(token.value))

    def LITERAL_BOOLEAN(self, token: Token) -> EvaluationResult:
        return EvaluationResult(bool(token.value))

    def LITERAL_NULL(self, token: Token) -> EvaluationResult:
        return EvaluationResult(None)
