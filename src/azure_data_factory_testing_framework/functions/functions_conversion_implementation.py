from typing import Any


def coalesce(args: list) -> Any:  # noqa: ANN401
    return next((arg for arg in args if arg is not None), None)


def json(argument: Any) -> Any:  # noqa: ANN401
    return argument


def string(input_str: Any) -> str:  # noqa: ANN401
    return input_str
