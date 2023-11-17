from typing import Any


def or_(a: Any, b: Any) -> Any:  # noqa: ANN401
    return a or b


def not_(value: Any) -> bool:  # noqa: ANN401
    return not value


def greater_or_equals(a: Any, b: Any) -> bool:  # noqa: ANN401
    return a >= b


def equals(a: Any, b: Any) -> bool:  # noqa: ANN401
    return a == b
