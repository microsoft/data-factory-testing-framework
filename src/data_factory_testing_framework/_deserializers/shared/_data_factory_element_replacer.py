from typing import Any

from data_factory_testing_framework.models import DataFactoryElement


def _find_and_replace_expressions_in_dict(obj: any, visited: list = None) -> None:
    if visited is None:
        visited = []

    if obj in visited:
        return

    visited.append(obj)

    # Attributes
    attribute_names = [
        attribute for attribute in dir(obj) if not attribute.startswith("_") and not callable(getattr(obj, attribute))
    ]
    for attribute_name in attribute_names:
        attribute = getattr(obj, attribute_name)
        if attribute is None:
            continue

        if _is_obj_expression_dict(attribute):
            value = _get_obj_expression_value(attribute)
            setattr(obj, attribute_name, DataFactoryElement(value))
        else:
            _find_and_replace_expressions_in_dict(attribute, visited)

    # Dictionary
    if isinstance(obj, dict):
        for key in obj.keys():
            if _is_obj_expression_dict(obj[key]):
                value = _get_obj_expression_value(obj[key])
                obj[key] = DataFactoryElement(value)
                continue

            _find_and_replace_expressions_in_dict(obj[key], visited)

    # List
    if isinstance(obj, list):
        for item in obj:
            if _is_obj_expression_dict(item):
                value = _get_obj_expression_value(item)
                obj[obj.index(item)] = DataFactoryElement(value)
                continue

            _find_and_replace_expressions_in_dict(item, visited)


def _is_obj_expression_dict(obj: Any) -> bool:  # noqa: ANN401
    return (
        isinstance(obj, dict)
        and ("type" in obj.keys())
        and (obj["type"] == "Expression")
        and (("value" in obj.keys()) or ("content" in obj.keys()))
        and len(obj.keys()) == 2
    )


def _get_obj_expression_value(obj: Any) -> Any:  # noqa: ANN401
    if "value" in obj.keys():
        return obj["value"]

    if "content" in obj.keys():
        return obj["content"]

    raise ValueError("Expression object does not contain a value or content key")
