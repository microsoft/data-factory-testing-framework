from typing import Any, Union

import data_factory_testing_framework.functions.functions_logical_implementation as logical_functions
import pytest
from pytest import param


@pytest.mark.parametrize(
    "expression1, expression_2, expected",
    [
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, False),
    ],
)
def test_and(expression1: bool, expression_2: bool, expected: bool) -> None:
    # Act
    actual = logical_functions.and_(expression1, expression_2)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    "object1, object2, expected",
    [
        (True, 1, True),
        ("abc", "abcd", False),
    ],
)
def test_equals(object1: Any, object2: Any, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.equals(object1, object2)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "compare_to", "expected"],
    [
        param(10, 5, True),
        param("apple", "banana", False),
    ],
)
def test_greater(value: Any, compare_to: Any, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.greater(value, compare_to)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "compare_to", "expected"],
    [
        param(10, 5, True),
        param(5, 10, False),
        param(5, 5, True),
    ],
)
def test_greater_or_equals(value: Any, compare_to: Any, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.greater_or_equals(value, compare_to)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["expression", "value_if_true", "value_if_false", "expected"],
    [
        param(True, "yes", "no", "yes"),
        param(False, "yes", "no", "no"),
    ],
)
def test_if(expression: bool, value_if_true: Any, value_if_false: Any, expected: Any) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.if_(expression, value_if_true, value_if_false)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "compare_to", "expected"],
    [
        param(5, 10, True),
        param(10, 5, False),
        param(10, 10, False),
        param("apple", "banana", True),
        param("banana", "apple", False),
        param("apple", "apple", False),
    ],
)
def test_less(value: Union[int, float, str], compare_to: Union[int, float, str], expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.less(value, compare_to)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "compare_to", "expected"],
    [
        param(5, 10, True),
        param(10, 5, False),
        param(10, 10, True),
        param("apple", "banana", True),
        param("banana", "apple", False),
        param("apple", "apple", True),
    ],
)
def test_less_or_equals(value: Union[int, float, str], compare_to: Union[int, float, str], expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.less_or_equals(value, compare_to)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["expression", "expected"],
    [
        param(True, False),
        param(False, True),
    ],
)
def test_not(expression: bool, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.not_(expression)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["expression1", "expression2", "expected"],
    [
        param(True, True, True),
        param(True, False, True),
        param(False, True, True),
        param(False, False, False),
    ],
)
def test_or(expression1: bool, expression2: bool, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = logical_functions.or_(expression1, expression2)

    # Assert
    assert actual == expected
