"""String functions implementation based on Expression Language.

See https://learn.microsoft.com/en-us/azure/data-factory/control-flow-expression-language-functions
"""


import uuid
from typing import Literal, Optional


def concat(*args: list[str]) -> str:
    """Combine two or more strings, and return the combined string."""
    return "".join(args)


def ends_with(text: str, search_text: str) -> bool:
    """Check whether a string ends with a specific substring.

    Return true when the substring is found, or return false when not found. This function is not case-sensitive.
    """
    return text.lower().endswith(search_text.lower())


def guid(format_: Optional[Literal["N", "D", "B", "P", "X"]] = None) -> str:  # noqa: A002
    """Generate a globally unique identifier (GUID) as a string, for example, "c2ecc88d-88c8-4096-912c-d6f2e2b138ce"."""
    if format_ is None or format_ == "":
        format_ = "D"

    uuid_value = uuid.uuid4()

    if format_ == "N":
        return str(uuid_value).replace("-", "")
    elif format_ == "D":
        return str(uuid_value)
    elif format_ == "B":
        return f"{{{str(uuid_value)}}}"
    elif format_ == "P":
        return f"({str(uuid_value)})"
    elif format_ == "X":
        node_bytes = uuid_value.node.to_bytes(6, "big")
        return (
            "{"
            f"0x{uuid_value.time_low:08x},"
            f"0x{uuid_value.time_mid:04x},"
            f"0x{uuid_value.time_hi_version:04x},"
            "{"
            f"0x{uuid_value.clock_seq_hi_variant:02x},"
            f"0x{uuid_value.clock_seq_low:02x},"
            f"0x{node_bytes[0]:02x},"
            f"0x{node_bytes[1]:02x},"
            f"0x{node_bytes[2]:02x},"
            f"0x{node_bytes[3]:02x},"
            f"0x{node_bytes[4]:02x},"
            f"0x{node_bytes[5]:02x}"
            "}}"
        )
    else:
        raise ValueError(f"Invalid format: {format_}")


def index_of(text: str, search_text: str) -> int:
    """Return the starting position or index value for a substring.

    This function is not case-sensitive, and indexes start with the number 0.
    """
    try:
        return text.lower().index(search_text.lower())
    except ValueError:
        return -1


def last_index_of(text: str, search_text: str) -> int:
    """Return the starting position or index value for the last occurrence of a substring.

    This function is not case-sensitive, and indexes start with the number 0.
    """
    try:
        return text.lower().rindex(search_text.lower())
    except ValueError:
        return -1


def replace(text: str, old_text: str, new_text: str) -> str:
    """Replace a substring with the specified string, and return the result string.

    This function is case-sensitive.
    """
    return text.replace(old_text, new_text)


def split(text: str, delimiter: str) -> list[str]:
    """Return an array that contains substrings, separated by commas, based on the specified delimiter character in the original string."""
    return text.split(delimiter)


def starts_with(text: str, search_text: str) -> bool:
    """Check whether a string starts with a specific substring.

    Return true when the substring is found, or return false when not found. This function is not case-sensitive.
    """
    return text.lower().startswith(search_text.lower())


def substring(text: str, start_index: int, length: int) -> str:
    """Return characters from a string, starting from the specified position, or index.

    Index values start with the number 0.
    """
    return text[start_index : start_index + length]


def to_lower(text: str) -> str:
    """Return a string in lowercase format.

    If a character in the string doesn't have a lowercase version, that character stays unchanged in the returned string.
    """
    return text.lower()


def to_upper(text: str) -> str:
    """Return a string in uppercase format.

    If a character in the string doesn't have an uppercase version, that character stays unchanged in the returned string.
    """
    return text.upper()


def trim(text: str) -> str:
    """Removes all leading and trailing white-space characters from the specified string."""
    return text.strip()
