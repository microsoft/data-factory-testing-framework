from typing import Any, Union


def and_(expression1: bool, expression2: bool) -> bool:
    """Check whether both expressions are true.

    Return true when both expressions are true, or return false when at least one expression is false.
    """
    return expression1 and expression2


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


def if_(expression: bool, value_if_true: Any, value_if_false: Any) -> Any:  # noqa: ANN401
    """Check whether an expression is true or false. Based on the result, return a specified value."""
    return value_if_true if expression else value_if_false


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


def or_(a: Any, b: Any) -> Any:  # noqa: ANN401
    """Check whether at least one expression is true. Return true when at least one expression is true, or return false when both are false."""
    return a or b
