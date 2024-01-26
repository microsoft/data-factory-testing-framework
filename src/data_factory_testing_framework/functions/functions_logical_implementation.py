from typing import Any, Union


def equals(object1: Any, object2: Any) -> bool:  # noqa: ANN401
    """Check whether both values, expressions, or objects are equivalent.

    Return true when both are equivalent, or return false when they're not equivalent.
    """
    return object1 == object2


def greater(value: Any, compare_to: Any) -> bool:  # noqa: ANN401
    """Check whether the first value is greater than the second value.

    Return true when the first value is more, or return false when less.
    """
    return value > compare_to


def greater_or_equals(value: Any, compare_to: Any) -> bool:  # noqa: ANN401
    """Check whether the first value is greater than or equal to the second value.

    Return true when the first value is greater or equal, or return false when the first value is less.
    """
    return value >= compare_to


def less(value: Union[int, float, str], compare_to: Union[int, float, str]) -> bool:  # noqa: ANN401
    """Check whether the first value is less than the second value.

    Return true when the first value is less, or return false when the first value is more.
    """
    return value < compare_to


def less_or_equals(value: Union[int, float, str], compare_to: Union[int, float, str]) -> bool:  # noqa: ANN401
    """Check whether the first value is less than or equal to the second value.

    Return true when the first value is less than or equal, or return false when the first value is more.
    """
    return value <= compare_to


def not_(value: Any) -> bool:  # noqa: ANN401
    """Check whether an expression is false. Return true when the expression is false, or return false when true."""
    return not value
