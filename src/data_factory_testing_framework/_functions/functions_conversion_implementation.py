import base64 as base64_lib
import json as json_lib
from typing import Any, Union
from urllib.parse import quote, unquote

import xmltodict
from lxml import etree


def array(value: Union[str, list]) -> list:
    """Return an array from a single specified input. For multiple inputs, see createArray()."""
    if isinstance(value, list):
        return value

    return [value]


def base64(value: str) -> str:
    """Return the base64-encoded version for a string."""
    return base64_lib.b64encode(value.encode("utf-8")).decode("utf-8")


def base64_to_binary(value: str) -> str:
    """Return the binary version for a base64-encoded string."""
    bytes_value = value.encode("utf-8")
    return "".join(f"{byte:08b}" for byte in bytes_value)


def base64_to_string(value: str) -> str:
    """Return the string version for a base64-encoded string, effectively decoding the base64 string.

    Use this function rather than decodeBase64(). Although both functions work the same way, base64ToString() is preferred.
    """
    return base64_lib.b64decode(value).decode("utf-8")


def binary(value: str) -> str:
    """Return the binary version for a string."""
    bytes_value = value.encode("utf-8")
    return "".join(f"{byte:08b}" for byte in bytes_value)


def bool_(value: Any) -> bool:  # noqa: ANN401
    """Return the Boolean version for a value."""
    return bool(value)


def coalesce(*objects: Any) -> Any:  # noqa: ANN401
    """Return the first non-null value from one or more parameters.

    Returns the first non-null (or non-empty for string) expression
    """
    for obj in objects:
        if obj is not None and obj != "":
            return obj

    return None


def create_array(*objects: Any) -> list:  # noqa: ANN401
    """Return an array from multiple inputs. For single input arrays, see array()."""
    return list(objects)


def data_uri(value: str) -> str:
    """Return a data uniform resource identifier (URI) for a string."""
    return f"data:text/plain;charset=utf-8;base64,{base64_lib.b64encode(value.encode('utf-8')).decode('utf-8')}"


def data_uri_to_binary(value: str) -> str:
    """Return the binary version for a data uniform resource identifier (URI).

    Use this function rather than decodeDataUri(). Although both functions work the same way, dataUriBinary() is preferred.
    """
    return base64_to_binary(value)


def data_uri_to_string(value: str) -> str:
    """Return the string version for a data uniform resource identifier (URI)."""
    base64_str = value.split(",")[1]
    return base64_to_string(base64_str)


def decode_base64(value: str) -> str:
    """Return the string version for a base64-encoded string, effectively decoding the base64 string.

    Consider using base64ToString() rather than decodeBase64(). Although both functions work the same way, base64ToString() is preferred.
    """
    return base64_lib.b64decode(value).decode("utf-8")


def decode_data_uri(value: str) -> str:
    """Return the binary version for a data uniform resource identifier (URI).

    Consider using dataUriToBinary(), rather than decodeDataUri(). Although both functions work the same way, dataUriToBinary() is preferred.
    """
    return base64_to_binary(value)


def decode_uri_component(value: str) -> str:
    """Return a string that replaces escape characters with decoded versions."""
    return unquote(value)


def encode_uri_component(value: str) -> str:
    """Return a string that replaces special characters with escaped versions."""
    return quote(value, safe="~()*!.'", encoding="utf-8")


def float_(value: Any) -> float:  # noqa: ANN401
    """Convert a string version for a floating-point number to an actual floating point number."""
    return float(value)


def int_(value: Any) -> int:  # noqa: ANN401
    """Return the integer version for a string."""
    return int(value)


def json(value: Union[str, etree.ElementBase]) -> Any:  # noqa: ANN401
    """Return the object version for a JSON string."""
    if isinstance(value, etree.ElementBase):
        elem_str = etree.tostring(value, encoding="utf-8", short_empty_elements=False).decode("utf-8")
        obj = xmltodict.parse(elem_str)
        return obj

    return json_lib.loads(value)


def string(value: Any) -> str:  # noqa: ANN401
    """Return the string version for a value."""
    if isinstance(value, dict) or isinstance(value, list):
        return json_lib.dumps(value)

    return str(value)


def uri_component(value: str) -> str:
    """Return a string that replaces special characters with escaped versions."""
    return quote(value, safe="~()*!.'", encoding="utf-8")


def uri_component_to_binary(value: str) -> str:
    """Return the binary version for a URI component."""
    return base64_to_binary(f'"{value}"')


def uri_component_to_string(value: str) -> str:
    """Return the string version for a URI component."""
    return unquote(value)


def xml(value: str) -> etree.ElementBase:
    """Return the object version for an XML string."""
    # TODO: xml support is not sufficient yet
    # we do not match the expression language of Fabric/ADF yet
    return etree.fromstring(value)


def xpath(value: etree.ElementBase, expression: str) -> list[etree.ElementBase]:
    """Return the object version for an XML string."""
    # TODO: xpath support is not sufficient yet
    # we do not match the expression language of Fabric/ADF yet
    return value.xpath(expression)
