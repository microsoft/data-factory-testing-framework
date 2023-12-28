from typing import Any, List, Union


def contains(collection: Union[str, list, dict], value: Any) -> bool:  # noqa: ANN401
    """Check whether a collection has a specific item. Return true when the item is found, or return false when not found.

    This function is case-sensitive.
    """
    if isinstance(collection, str):
        return value in collection

    if isinstance(collection, list):
        if value in collection:
            return True

    if isinstance(collection, dict):
        if value in collection.keys():
            return True
    return False


def empty(collection: Union[str, list]) -> bool:
    """Check whether a collection is empty. Return true when the collection is empty, or return false when not empty."""
    # TODO: we do not support Object - how does ADF/Fabric handle this.
    return len(collection) == 0


def first(collection: Union[str, list]) -> Any:  # noqa: ANN401
    """Return the first item from a string or array.

    Returns None if collection is empty.
    """
    if isinstance(collection, str) or isinstance(collection, list):
        if len(collection) > 0:
            return collection[0]
        else:
            return None
    # TODO: check default checks.
    return None


def intersection(*collections: Union[str, list]) -> list:
    """Return a collection that has only the common items across the specified collections.

    To appear in the result, an item must appear in all the collections passed to this function.
    If one or more items have the same name, the last item with that name appears in the result.
    """
    # TODO: validate this is correct.
    if len(collections) == 0:
        return []

    # TODO: what if only single collection
    if len(collections) == 1:
        raise ValueError("Only one collection passed to intersection")

    # All collections must be of the same type
    if not all(isinstance(collection, type(collections[0])) for collection in collections):
        raise ValueError("All collections must be of the same type")

    # Check if all collections are of type str or list
    if not isinstance(collections[0], str) and not isinstance(collections[0], list):
        raise ValueError("Only str and list are supported")

    output_type = type(collections[0])

    base_collection = collections[0]

    for collection in collections[1:]:
        intersection = [value for value in base_collection if value in collection]
        base_collection = intersection

    if output_type == str:
        return "".join(intersection)
    else:
        return intersection


def join(collection: list, delimiter: str) -> str:
    """Return a string that has all the items from an array and has each character separated by a delimiter."""
    if not isinstance(collection, list):
        raise ValueError("Only list is supported")

    if not isinstance(delimiter, str):
        raise ValueError("Only str is supported")

    return delimiter.join(collection)


def last(collection: Union[str, list]) -> Any:  # noqa: ANN401
    """Return the last item from a collection."""
    if isinstance(collection, str) or isinstance(collection, list):
        if len(collection) > 0:
            return collection[-1]
        else:
            return None


def length(collection: Union[str, list]) -> int:
    """Return the number of items in a collection."""
    if isinstance(collection, str) or isinstance(collection, list):
        return len(collection)
    else:
        return 0


def skip(collection: list, count: int) -> Union[str, list]:
    """Remove items from the front of a collection, and return all the other items."""
    if not isinstance(collection, list):
        raise ValueError("Only list is supported")

    if not isinstance(count, int):
        raise ValueError("Only int is supported")

    if count < 0:
        raise IndexError("Count must be greater than or equal to 0")

    if count > len(collection):
        raise IndexError("Count must be less than or equal to the length of the collection")

    return collection[count:]


def take(collection: Union[str, list], count: int) -> Union[str, list]:
    """Return the specified number of items from the front of a collection."""
    if not isinstance(collection, str) and not isinstance(collection, list):
        raise ValueError("Only str and list are supported")

    if not isinstance(count, int):
        raise ValueError("Only int is supported")

    if count < 0:
        raise IndexError("Count must be greater than or equal to 0")

    if count > len(collection):
        raise IndexError("Count must be less than or equal to the length of the collection")

    return collection[:count]


def union(*collections: list) -> list:  # noqa: ANN401
    """Return a collection that has all the items from the specified collections.

    To appear in the result, an item can appear in any collection passed to this function.
    If one or more items have the same name, the last item with that name appears in the result.
    """
    if len(collections) < 2:
        raise ValueError(
            (
                "The function 'union' expects either a comma separated list of arrays or a comma separated list of objects as its parameters."
                f"The function was invoked with '{len(collections)}' parameter(s)."
            )
        )

    if not all([isinstance(collection, list) for collection in collections]):
        raise ValueError("All collections must be of type list. Ensure the arguments passed to union are lists.")

    union_collection = []
    for collection in collections:
        union_collection = _remove_duplicates(union_collection + collection)

    return union_collection


def _remove_duplicates(collection: List[Any]) -> List[Any]:
    unique_list = []

    for collection_item in collection:
        if collection_item not in unique_list:
            unique_list.append(collection_item)

    return unique_list
