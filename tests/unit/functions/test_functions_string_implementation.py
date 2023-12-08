import data_factory_testing_framework.functions.functions_string_implementation as string_functions
import pytest


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        (["a", "b", "c"], "abc"),
        (["a", "b", "c", "d"], "abcd"),
    ],
)
def test_concat(
    args: list[str],
    expected: str,
) -> None:
    # Act
    actual = string_functions.concat(*args)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "search_text", "expected"],
    [
        ("abc", "a", False),
        ("abc", "c", True),
        ("abc", "b", False),
        ("abc", "C", True),
        ("abc", "d", False),
        ("abcabc", "Bc", True),
    ],
)
def test_ends_with(text: str, search_text: str, expected: bool) -> None:
    # Act
    actual = string_functions.ends_with(text, search_text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["uuid_format", "expected"],
    [
        (None, "0b79217c-c85d-4f19-8c37-56a15b8143ba"),
        ("", "0b79217c-c85d-4f19-8c37-56a15b8143ba"),
        ("N", "0b79217cc85d4f198c3756a15b8143ba"),
        ("D", "0b79217c-c85d-4f19-8c37-56a15b8143ba"),
        ("B", "{0b79217c-c85d-4f19-8c37-56a15b8143ba}"),
        ("P", "(0b79217c-c85d-4f19-8c37-56a15b8143ba)"),
        ("X", "{0x0b79217c,0xc85d,0x4f19,{0x8c,0x37,0x56,0xa1,0x5b,0x81,0x43,0xba}}"),
    ],
)
def test_guid(uuid_format: str, expected: str, monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    import uuid

    uuid_mock = uuid.UUID("0b79217c-c85d-4f19-8c37-56a15b8143ba")

    monkeypatch.setattr(uuid, "uuid4", lambda: uuid_mock)

    # Act
    actual = string_functions.guid(uuid_format)

    # Assert
    assert expected == actual


@pytest.mark.parametrize(
    ["text", "search_text", "expected"],
    [
        ("abc", "c", 2),
        ("abc", "b", 1),
        ("abc", "C", 2),
        ("abc", "d", -1),
        ("abcabc", "a", 0),
    ],
)
def test_index_of(text: str, search_text: str, expected: int) -> None:
    # Act
    actual = string_functions.index_of(text, search_text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "search_text", "expected"],
    [
        ("abc", "c", 2),
        ("abc", "b", 1),
        ("abc", "C", 2),
        ("abc", "d", -1),
        ("abcabc", "a", 3),
    ],
)
def test_last_index_of(text: str, search_text: str, expected: int) -> None:
    # Act
    actual = string_functions.last_index_of(text, search_text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "old_text", "new_text", "expected"],
    [
        ("abc", "c", "d", "abd"),
        ("abc", "b", "d", "adc"),
        ("abc", "C", "d", "abc"),
        ("abc", "d", "e", "abc"),
        ("abcabc", "a", "d", "dbcdbc"),
    ],
)
def test_replace(text: str, old_text: str, new_text: str, expected: str) -> None:
    # Act
    actual = string_functions.replace(text, old_text, new_text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "delimiter", "expected"],
    [
        ("abc", "c", ["ab", ""]),
        ("abc", "b", ["a", "c"]),
        ("abc", "C", ["abc"]),
        ("abc", "d", ["abc"]),
        ("abcabc", "a", ["", "bc", "bc"]),
    ],
)
def test_split(text: str, delimiter: str, expected: list[str]) -> None:
    # Act
    actual = string_functions.split(text, delimiter)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "search_text", "expected"],
    [
        ("abc", "a", True),
        ("abc", "c", False),
        ("abc", "b", False),
        ("abc", "C", False),
        ("abc", "d", False),
        ("Abcabc", "Ab", True),
    ],
)
def test_starts_with(text: str, search_text: str, expected: bool) -> None:
    # Act
    actual = string_functions.starts_with(text, search_text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "start_index", "length", "expected"],
    [
        ("abc", 0, 1, "a"),
        ("abc", 0, 2, "ab"),
        ("abc", 0, 3, "abc"),
        ("abc", 1, 1, "b"),
        ("abc", 1, 2, "bc"),
        ("abc", 2, 1, "c"),
        ("abc", 2, 2, "c"),
        ("abc", 3, 1, ""),
        ("abc", 4, 1, ""),
        ("abc", 0, 0, ""),
        ("abc", 1, 0, ""),
        ("abc", 2, 0, ""),
        ("abc", 3, 0, ""),
        ("abc", 4, 0, ""),
    ],
)
def test_substring(text: str, start_index: int, length: int, expected: str) -> None:
    # Act
    actual = string_functions.substring(text, start_index, length)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "expected"],
    [
        ("abc", "abc"),
        ("ABC", "abc"),
        ("AbC", "abc"),
        ("$AbC", "$abc"),
        ("A&C", "a&c"),
    ],
)
def test_to_lower(text: str, expected: str) -> None:
    # Act
    actual = string_functions.to_lower(text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "expected"],
    [
        ("abc", "ABC"),
        ("ABC", "ABC"),
        ("AbC", "ABC"),
        ("$AbC", "$ABC"),
        ("a7c", "A7C"),
    ],
)
def test_to_upper(text: str, expected: str) -> None:
    # Act
    actual = string_functions.to_upper(text)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["text", "expected"],
    [
        ("abc", "abc"),
        (" abc", "abc"),
        ("abc ", "abc"),
        (" abc ", "abc"),
        ("  abc  ", "abc"),
    ],
)
def test_trim(text: str, expected: str) -> None:
    # Act
    actual = string_functions.trim(text)

    # Assert
    assert actual == expected
