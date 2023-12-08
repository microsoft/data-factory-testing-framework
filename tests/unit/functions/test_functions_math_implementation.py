import random
from typing import Union

import data_factory_testing_framework.functions.functions_math_implementation as math_functions
import pytest


@pytest.mark.parametrize(
    ["summand_1", "summand_2", "expected"],
    [
        (1, 1.5, 2.5),
        (-5, 2, -3),
        (1, 4, 5),
    ],
)
def test_add(
    summand_1: Union[int, float],
    summand_2: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.add(summand_1, summand_2)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["summand_1", "summand_2"],
    [
        (None, 1),
    ],
)
def test_add_with_typeerror(
    summand_1: Union[int, float],
    summand_2: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.add(summand_1, summand_2)


@pytest.mark.parametrize(
    ["dividend", "divisor", "expected"],
    [
        (10, 5, 2),
        (11, 5, 2),
        (5.5, 5, 1.1),
        (4.5, 1.5, 3),
        (4.8, 2.1, 2.2857142857142856),
    ],
)
def test_div(
    dividend: Union[int, float],
    divisor: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.div(dividend, divisor)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["dividend", "divisor"],
    [
        (5, 0),
    ],
)
def test_div_with_zerodivisionerror(
    dividend: Union[int, float],
    divisor: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(ZeroDivisionError):
        math_functions.div(dividend, divisor)


@pytest.mark.parametrize(
    ["dividend", "divisor"],
    [
        (None, 1),
    ],
)
def test_div_with_typeerror(
    dividend: Union[int, float],
    divisor: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.div(dividend, divisor)


@pytest.mark.parametrize(
    ["arg1", "args", "expected"],
    [
        ([1, 2, 3], (), 3),
        ([1, 2.4, 3.6], (), 3.6),
        ([-1], (), -1),
        (1, (2, 3.5), 3.5),
        (1, (), 1),
    ],
)
def test_max(
    arg1: Union[list, int, float],
    args: tuple,
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.max_(arg1, *args)

    # Assert
    assert actual == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    ["arg1", "args"],
    [
        (None, ()),
        ([None], ()),
    ],
)
def test_max_with_typeerror(arg1: Union[list, int, float], args: tuple) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.max_(arg1, *args)


@pytest.mark.parametrize(
    ["arg1", "args", "expected"],
    [([1, 2, 3], (), 1), ([1.2, 2.4, 3.6], (), 1.2), ([-1], (), -1), (1, (2, 3.5), 1), (1, (), 1)],
)
def test_min(
    arg1: Union[list, int, float],
    args: tuple,
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.min_(arg1, *args)

    # Assert
    assert actual == expected


@pytest.mark.xfail
@pytest.mark.parametrize(
    ["arg1", "args"],
    [
        (None, ()),
        ([None], ()),
    ],
)
def test_min_with_typeerror(arg1: Union[list, int, float], args: tuple) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.min_(arg1, *args)


@pytest.mark.parametrize(
    ["dividend", "divisor", "expected"],
    [
        (-3, 2, 1),
        (3.5, 2.4, 1.1),
        (3.5, 2, 1.5),
        (0, 2, 0),
    ],
)
def test_mod(
    dividend: Union[int, float],
    divisor: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.mod(dividend, divisor)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["dividend", "divisor"],
    [
        (5, 0),
        (2.5, 0),
    ],
)
def test_mod_with_zerodivisionerror(
    dividend: Union[int, float],
    divisor: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(ZeroDivisionError):
        math_functions.mod(dividend, divisor)


@pytest.mark.parametrize(
    ["dividend", "divisor"],
    [
        (None, 1),
        (1, None),
        (None, None),
    ],
)
def test_mod_with_typeerror(
    dividend: Union[int, float],
    divisor: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.mod(dividend, divisor)


@pytest.mark.parametrize(
    ["multiplicand1", "multiplicand2", "expected"],
    [
        (3, 2, 6),
        (3.5, 2.4, 8.4),
        (3.5, -2, -7),
        (0, 2, 0),
    ],
)
def test_mul(
    multiplicand1: Union[int, float],
    multiplicand2: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.mul(multiplicand1, multiplicand2)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["multiplicand1", "multiplicand2"],
    [
        (None, 1),
        (1, None),
        (None, None),
    ],
)
def test_mul_with_typeerror(
    multiplicand1: Union[int, float],
    multiplicand2: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.mul(multiplicand1, multiplicand2)


@pytest.mark.parametrize(
    ["min_value", "max_value", "expected"],
    [
        (2, 8, 3),
    ],
)
def test_rand(
    min_value: Union[int, float],
    max_value: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    random.seed(1)
    actual = math_functions.rand(min_value, max_value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["min_value", "max_value"],
    [
        (None, 1),
        (1, None),
        (None, None),
    ],
)
def test_rand_with_typeerror(
    min_value: Union[int, float],
    max_value: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.rand(min_value, max_value)


@pytest.mark.parametrize(
    ["start_index", "count", "expected"],
    [
        (5, 3, [5, 6, 7]),
        (-1, 3, [-1, 0, 1]),
    ],
)
def test_range(
    start_index: Union[int, float],
    count: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.range_(start_index, count)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["start_index", "count"],
    [
        (None, 1),
        (1, None),
        (None, None),
    ],
)
def test_range_with_typeerror(
    start_index: Union[int, float],
    count: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.range_(start_index, count)


@pytest.mark.parametrize(
    ["minuend", "subtrahend", "expected"],
    [
        (5, 3, 2),
        (-1, 3.5, -4.5),
    ],
)
def test_sub(
    minuend: Union[int, float],
    subtrahend: Union[int, float],
    expected: Union[int, float],
) -> None:
    # Act
    actual = math_functions.sub(minuend, subtrahend)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["minuend", "subtrahend"],
    [
        (None, 1),
        (1, None),
        (None, None),
    ],
)
def test_sub_with_typeerror(
    minuend: Union[int, float],
    subtrahend: Union[int, float],
) -> None:
    # Assert
    with pytest.raises(TypeError):
        math_functions.sub(minuend, subtrahend)
