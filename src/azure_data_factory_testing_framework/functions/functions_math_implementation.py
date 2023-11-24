import random
from typing import Union


def add(summand_1: Union[int, float], summand_2: Union[int, float]) -> Union[int, float]:
    """Return the result from adding two numbers."""
    return summand_1 + summand_2


def div(dividend: Union[int, float], divisor: Union[int, float]) -> Union[int, float]:
    """Return the integer result from dividing two numbers. If both the inputs are integers, the result will be an integer."""
    if isinstance(dividend, int) and isinstance(divisor, int):
        return dividend // divisor
    return dividend / divisor


def max_(arg1: Union[list, int, float], *args: Union[int, float]) -> Union[int, float]:
    """Return the highest value from an array with numbers that is inclusive at both ends."""
    if isinstance(arg1, list):
        return max(arg1)
    if len(args) == 0:
        return arg1
    return max(arg1, *args)


def min_(arg1: Union[list, int, float], *args: Union[int, float]) -> Union[int, float]:
    """Return the lowest value from a set of numbers or an array."""
    if isinstance(arg1, list):
        return min(arg1)
    if len(args) == 0:
        return arg1
    return min(arg1, *args)


def mod(dividend: Union[int, float], divisor: Union[int, float]) -> Union[int, float]:
    """Return the remainder from dividing two numbers."""
    return dividend % divisor


def mul(multiplicand1: Union[int, float], multiplicand2: Union[int, float]) -> Union[int, float]:
    """Return the product from multiplying two numbers."""
    return multiplicand1 * multiplicand2


def rand(min_value: int, max_value: int) -> int:
    """Return a random integer from a specified range, which is inclusive only at the starting end."""
    return random.randint(min_value, max_value - 1)


def range_(start_index: int, count: int) -> list:
    """Return an integer array that starts from a specified integer."""
    return list(range(start_index, start_index + count))


def sub(minuend: Union[int, float], subtrahend: Union[int, float]) -> Union[int, float]:
    """Return the result from subtracting the second number from the first number."""
    return minuend - subtrahend
