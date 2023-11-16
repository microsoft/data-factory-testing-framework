import re
from typing import Union

from azure_data_factory_testing_framework.functions.function_argument import FunctionArgument
from azure_data_factory_testing_framework.functions.function_call import FunctionCall

extract_func_regex = r"^@?{?([^()]+?)\((.*)\)}?$"


def parse_expression(expression: str) -> Union[FunctionCall, FunctionArgument]:
    match = re.match(extract_func_regex, expression, re.DOTALL)
    if not match:
        return FunctionArgument(expression)

    function_name = match.group(1).strip()
    if function_name in ["variables", "activity", "pipeline", "item"]:
        return FunctionArgument(expression)

    function_arguments_expression = match.group(2)

    start = 0
    in_quotes = False
    in_parenthesis = 0
    arguments = []
    for i in range(len(function_arguments_expression)):
        current_char = function_arguments_expression[i]
        next_char = function_arguments_expression[i + 1] if i < len(function_arguments_expression) - 1 else "\0"
        if current_char == "," and not in_quotes and in_parenthesis == 0:
            arguments.append(function_arguments_expression[start:i].replace("''", "'"))
            start = i + 1
            continue

        # Skip escaped single quotes
        if in_quotes and current_char == "'" and next_char == "'":
            i += 1
            continue

        if current_char == "'":
            in_quotes = not in_quotes

        if current_char == "(":
            in_parenthesis += 1

        if current_char == ")":
            in_parenthesis -= 1

        if i == len(function_arguments_expression) - 1:
            arguments.append(function_arguments_expression[start : i + 1].replace("''", "'"))

    return FunctionCall(
        function_name,
        list(map(parse_expression, [x.strip() for x in arguments])),
    )
