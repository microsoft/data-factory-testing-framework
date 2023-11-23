from typing import Any, Union

import azure_data_factory_testing_framework.functions.functions_collection_implementation as collection_functions
import pytest
from pytest import param


@pytest.mark.parametrize(
    ["collection", "value", "expected"],
    [
        param("abcdef", "cd", True, id="str_contains"),
        param("abcdef", "CD", False, id="str_contains_case_sensitive"),
        param(
            "abc8ef", 8, True, id="str_contains", marks=pytest.mark.xfail(raises=TypeError)
        ),  # TODO: Should this work, and if so what with list and dict?
        param(["a", "b", "c"], "b", True, id="list_contains"),
        param(["a", "b", "c"], "B", False, id="list_contains_case_sensitive"),
        param({"a": 1, "b": 2, "c": 3}, "b", True, id="dict_contains"),
        param({"a": 1, "b": 2, "c": 3}, "B", False, id="dict_contains_case_sensitive"),
    ],
)
def test_contains(collection: Union[str, list, dict], value: Any, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = collection_functions.contains(collection, value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "expected"],
    [
        param("abcdef", False, id="str_empty"),
        param("", True, id="str_empty"),
        param(["a", "b", "c"], False, id="list_empty"),
        param([], True, id="list_empty"),
    ],
)
def test_empty(collection: Union[str, list], expected: bool) -> None:
    # Act
    actual = collection_functions.empty(collection)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "expected"],
    [
        param(["a", "b", "c"], "a", id="list_first"),
        param("abcdef", "a", id="str_first"),
        param([1, 2, 3], 1, id="list_first_int"),
        param([], None, id="list_first_empty"),
        param("", None, id="str_first_empty"),
    ],
)
def test_first(collection: Union[str, list], expected: Any) -> None:  # noqa: ANN401
    # Act
    actual = collection_functions.first(collection)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collections", "expected"],
    [
        param([["a", "b", "c"], ["b", "c", "d"]], ["b", "c"], id="list_intersection"),
        param(["abcdef", "cdefgh"], "cdef", id="str_intersection"),
    ],
)
def test_intersection(collections: list[Union[str, list]], expected: Union[str, list]) -> None:
    # Act
    actual = collection_functions.intersection(*collections)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "delimiter", "expected"],
    [
        param(["a", "b", "c"], ",", "a,b,c", id="list_join"),
        param(["a", "b", "c"], "", "abc", id="list_join_empty_delimiter"),
        param(["a", "b", "c"], " ", "a b c", id="list_join_space_delimiter"),
    ],
)
def test_join(collection: list, delimiter: str, expected: str) -> None:
    # Act
    actual = collection_functions.join(collection, delimiter)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "expected"],
    [
        param(["a", "b", "c"], "c", id="list_last"),
        param("abcdef", "f", id="str_last"),
        param([1, 2, 3], 3, id="list_last_int"),
        param([], None, id="list_last_empty"),
        param("", None, id="str_last_empty"),
    ],
)
def test_last(collection: Union[str, list], expected: Any) -> None:  # noqa: ANN401
    # Act
    actual = collection_functions.last(collection)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "expected"],
    [
        param(["a", "b", "c"], 3, id="list_length"),
        param("abcdef", 6, id="str_length"),
        param([], 0, id="list_length_empty"),
        param("", 0, id="str_length_empty"),
        param(None, 0, id="str_length_none"),
    ],
)
def test_length(collection: Union[str, list], expected: int) -> None:  # noqa: ANN401
    # Act
    actual = collection_functions.length(collection)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "count", "expected"],
    [
        param(["a", "b", "c"], 2, ["c"], id="list_skip"),
        param([], 2, [], id="list_skip_empty", marks=pytest.mark.xfail(raises=IndexError)),
        param(None, 2, None, id="str_skip_none", marks=pytest.mark.xfail(raises=ValueError)),
    ],
)
def test_skip(collection: list, count: int, expected: list) -> None:
    # Act
    actual = collection_functions.skip(collection, count)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collection", "count", "expected"],
    [
        param(["a", "b", "c"], 2, ["a", "b"], id="list_take"),
        param([], 2, [], id="list_take_empty", marks=pytest.mark.xfail(raises=IndexError)),
        param(None, 2, None, id="str_take_none", marks=pytest.mark.xfail(raises=ValueError)),
    ],
)
def test_take(collection: Union[str, list], count: int, expected: list) -> None:
    # Act
    actual = collection_functions.take(collection, count)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["collections", "expected"],
    [
        param([["a", "b", "c"], ["b", "c", "d"]], ["a", "b", "c", "d"], id="list_union"),
        param(
            [["a", "b", "c"], ["b", "c", "d"], ["a", "b", "c", "d"]], ["a", "b", "c", "d"], id="list_union_duplicates"
        ),
        param([["c", "b", "a"], ["d", "c", "b"]], ["c", "b", "a", "d"], id="list_union_order"),
        param([[1, 2, 3], [1, 2, 10, 101]], [1, 2, 3, 10, 101], id="list_union_int"),
        param([[1, 1, 1], [2, 3, 4]], [1, 2, 3, 4], id="list_union_int_duplicates"),
    ],
)
def test_union(collections: list[list], expected: Any) -> None:  # noqa: ANN401
    # Act
    actual = collection_functions.union(*collections)

    # Assert
    assert actual == expected
