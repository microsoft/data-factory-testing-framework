from typing import Any, Union

import data_factory_testing_framework.functions.functions_conversion_implementation as conversion_functions
import pytest
from lxml import etree
from pytest import param


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("hello", ["hello"]),
    ],
)
def test_array(value: str, expected: list) -> None:
    # Act
    actual = conversion_functions.array(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("hello", "aGVsbG8="),
    ],
)
def test_base64(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.base64(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("aGVsbG8=", "0110000101000111010101100111001101100010010001110011100000111101"),
    ],
)
def test_base64_to_binary(value: str, expected: bytes) -> None:
    # Act
    actual = conversion_functions.base64_to_binary(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("aGVsbG8=", "hello"),
    ],
)
def test_base64_to_string(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.base64_to_string(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("hello", "0110100001100101011011000110110001101111"),
    ],
)
def test_binary(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.binary(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(1, True),
        param(0, False),
    ],
)
def test_bool(value: Any, expected: bool) -> None:  # noqa: ANN401
    # Act
    actual = conversion_functions.bool_(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["objects", "expected"],
    [
        param([None, True, False], True),
        param([None, "hello", "world"], "hello"),
        param([None, None, None], None),
    ],
)
def test_coalesce(objects: list[Any], expected: Any) -> None:  # noqa: ANN401
    # Act
    actual = conversion_functions.coalesce(*objects)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["objects", "expected"],
    [
        param(["h", "e", "l", "l", "o"], ["h", "e", "l", "l", "o"]),
    ],
)
def test_create_array(objects: list[Any], expected: Any) -> None:  # noqa: ANN401
    # Act
    actual = conversion_functions.create_array(*objects)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("hello", "data:text/plain;charset=utf-8;base64,aGVsbG8="),
    ],
)
def test_data_uri(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.data_uri(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(
            "data:text/plain;charset=utf-8;base64,aGVsbG8=",
            (
                "01100100011000010111010001100001001110100111010001100101011110000111010000101111011100000"
                "1101100011000010110100101101110001110110110001101101000011000010111001001110011011001010111"
                "0100001111010111010101110100011001100010110100111000001110110110001001100001011100110110010"
                "10011011000110100001011000110000101000111010101100111001101100010010001110011100000111101"
            ),
        ),
    ],
)
def test_data_uri_to_binary(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.data_uri_to_binary(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("data:text/plain;charset=utf-8;base64,aGVsbG8=", "hello"),
    ],
)
def test_data_uri_to_string(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.data_uri_to_string(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("aGVsbG8=", "hello"),
    ],
)
def test_decode_base64(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.decode_base64(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(
            "data:text/plain;charset=utf-8;base64,aGVsbG8=",
            (
                "01100100011000010111010001100001001110100111010001100101011110000111010000101111011100000"
                "1101100011000010110100101101110001110110110001101101000011000010111001001110011011001010111"
                "0100001111010111010101110100011001100010110100111000001110110110001001100001011100110110010"
                "10011011000110100001011000110000101000111010101100111001101100010010001110011100000111101"
            ),
        ),
    ],
)
def test_decode_data_uri(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.decode_data_uri(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("http%3A%2F%2Fcontoso.com", "http://contoso.com"),
    ],
)
def test_decode_uri_component(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.decode_uri_component(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("http://contoso.com", "http%3A%2F%2Fcontoso.com"),
    ],
)
def test_encode_uri_component(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.encode_uri_component(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("10.333", 10.333),
    ],
)
def test_float(value: str, expected: float) -> None:
    # Act
    actual = conversion_functions.float_(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("10", 10),
    ],
)
def test_int(value: str, expected: int) -> None:
    # Act
    actual = conversion_functions.int_(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(
            "[1, 2, 3]",
            [1, 2, 3],
            marks=pytest.mark.xfail(
                reason="TODO: json to array conversion not supported as we do not support complex types"
            ),
        ),
        param(
            '{"fullName": "Sophia Owen"}',
            {"fullName": "Sophia Owen"},
            marks=pytest.mark.xfail(
                reason="TODO: json to object conversion not supported as we do not support complex types"
            ),
        ),
        param(
            etree.fromstring(
                '<?xml version="1.0"?> <root> <person id="1">'
                "<name>Sophia Owen</name> <occupation>Engineer</occupation> </person> </root>"
            ),
            {
                "?xml": {"@version": "1.0"},
                "root": {"person": [{"@id": "1", "name": "Sophia Owen", "occupation": "Engineer"}]},
            },
            marks=pytest.mark.xfail(reason="TODO: xml to json conversion implementation does not fully match yet"),
        ),
    ],
)
def test_json(value: Union[str, etree.fromstring], expected: object) -> None:
    # TODO: really unclear how we handle json objects (as no 'json' type exists in python)
    # Act
    actual = conversion_functions.json(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(10, "10"),
        param(
            {"name": "Sophie Owen"},
            '{ \\"name\\": \\"Sophie Owen\\" }',
            marks=pytest.mark.xfail(reason="TODO: objects to string do not match yet"),
        ),
    ],
)
def test_string(value: Any, expected: str) -> None:  # noqa: ANN401
    # Act
    actual = conversion_functions.string(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("http://contoso.com", "http%3A%2F%2Fcontoso.com"),
    ],
)
def test_uri_component(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.uri_component(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(
            "http%3A%2F%2Fcontoso.com",
            (
                "001000100110100001110100011101000111000000100101001100"
                "11010000010010010100110010010001100010010100110010010001"
                "10011000110110111101101110011101000110111101110011011011"
                "110010111001100011011011110110110100100010"
            ),
        ),
    ],
)
def test_uri_component_to_binary(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.uri_component_to_binary(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param("http%3A%2F%2Fcontoso.com", "http://contoso.com"),
    ],
)
def test_uri_component_to_string(value: str, expected: str) -> None:
    # Act
    actual = conversion_functions.uri_component_to_string(value)

    # Assert
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        param(
            '<?xml version="1.0"?> <root> <person id="1">'
            "<name>Sophia Owen</name> <occupation>Engineer</occupation> </person> </root>",
            etree.fromstring(
                (
                    '<?xml version="1.0"?> <root> <person id="1">'
                    "<name>Sophia Owen</name> <occupation>Engineer</occupation> </person> </root>"
                )
            ),
        ),
    ],
)
def test_xml(value: object, expected: etree.Element) -> None:
    # Act
    actual = conversion_functions.xml(value)

    # Assert
    assert etree.tostring(actual) == etree.tostring(expected)


@pytest.mark.parametrize(
    ["xml", "xpath", "expected"],
    [
        param(
            etree.fromstring(
                '<?xml version="1.0"?> <root> <person id="1"><name>Sophia Owen</name> <occupation>Engineer</occupation> </person> </root>'
            ),
            "root/person/name",
            "Sophia Owen",
            marks=pytest.mark.xfail(
                reason="TODO: xpath implementation does work yet due to different xml capabilities"
            ),
        ),
        param(
            etree.fromstring(
                (
                    '<?xml version="1.0"?> <produce> '
                    "<item> <count>1</count> <name>Apple</name> </item>"
                    "<item> <count>2</count> <name>Orange</name> </item>"
                    "<item> <count>3</count> <name>Banana</name> </item>"
                    "</produce>"
                )
            ),
            "sum(/produce/item/count)",
            6.0,  # TODO: this is a float, yet expressions return something else
        ),
        param(
            etree.fromstring(
                ('<?xml version="1.0"?> <file xmlns="http://contoso.com"> <location>Paris</location> </file>')
            ),
            '/*[name()="file"]/*[name()="location"]',
            '<location xmlns="https://contoso.com">Paris</location>',
            marks=pytest.mark.xfail(
                reason="TODO: xpath implementation does work yet due to different xml capabilities"
            ),
        ),
        param(
            etree.fromstring(
                ('<?xml version="1.0"?> <file xmlns="http://contoso.com"> <location>Paris</location> </file>')
            ),
            '/*[local-name()="file" and namespace-uri()="http://contoso.com"]/*[local-name()="location"]',
            '<location xmlns="https://contoso.com">Paris</location>',
            marks=pytest.mark.xfail(
                reason="TODO: xpath implementation does work yet due to different xml capabilities"
            ),
        ),
        param(
            etree.fromstring(
                ('<?xml version="1.0"?> <file xmlns="http://contoso.com"> <location>Paris</location> </file>')
            ),
            '/*[local-name()="file"]/*[local-name()="location"]',
            'string(/*[name()="file"]/*[name()="location"])',
            marks=pytest.mark.xfail(
                reason="TODO: xpath implementation does work yet due to different xml capabilities"
            ),
        ),
    ],
)
def test_xpath(xml: etree.Element, xpath: str, expected: Union[object, list]) -> None:
    # Act
    actual = conversion_functions.xpath(xml, xpath)

    # Assert
    assert actual == expected
