from typing import Any, Union

import data_factory_testing_framework._functions.functions_logical_implementation as logical_functions
import pytest
from pytest import param


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
