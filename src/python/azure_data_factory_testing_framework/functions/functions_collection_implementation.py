import json
from collections.abc import Iterable as IterableType
from typing import Any, Sized


# TODO: Add type annotations based on Fabric and ADF
def union(arg0, arg1):  # noqa: ANN001, ANN201
    return json.dumps(json.loads(arg0) + json.loads(arg1))


def empty(array: Sized) -> bool:  # noqa: ANN401
    return len(array) == 0


def contains(obj: Any, value: Any) -> bool:  # noqa: ANN401
    return (
        value in obj
        if isinstance(obj, dict)
        else value in obj
        if isinstance(obj, IterableType)
        else value in obj
        if isinstance(obj, str)
        else False
    )
