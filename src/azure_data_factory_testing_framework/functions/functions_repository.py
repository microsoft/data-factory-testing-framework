from typing import Callable, Dict

import azure_data_factory_testing_framework.functions.functions_collection_implementation as collection_functions
import azure_data_factory_testing_framework.functions.functions_conversion_implementation as conversion_functions
import azure_data_factory_testing_framework.functions.functions_date_implementation as date_functions
import azure_data_factory_testing_framework.functions.functions_logical_implementation as logical_functions
import azure_data_factory_testing_framework.functions.functions_math_implementation as math_functions
import azure_data_factory_testing_framework.functions.functions_string_implementation as string_functions


class FunctionsRepository:
    functions: Dict[str, Callable] = {
        "concat": string_functions.concat,
        "trim": string_functions.trim,
        "equals": logical_functions.equals,
        "json": conversion_functions.json,
        "contains": collection_functions.contains,
        "replace": string_functions.replace,
        "string": conversion_functions.string,
        "union": collection_functions.union,
        "coalesce": conversion_functions.coalesce,
        "or": logical_functions.or_,
        "utcnow": date_functions.utcnow,
        "ticks": date_functions.ticks,
        "sub": math_functions.sub,
        "div": math_functions.div,
        "greaterOrEquals": logical_functions.greater_or_equals,
        "not": logical_functions.not_,
        "empty": collection_functions.empty,
        "split": string_functions.split,
    }

    @staticmethod
    def register(function_name: str, function: Callable) -> None:
        FunctionsRepository.functions[function_name] = function
