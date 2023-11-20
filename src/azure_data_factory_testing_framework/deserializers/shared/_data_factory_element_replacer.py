from typing import Any

from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement


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
            setattr(obj, attribute_name, DataFactoryElement(attribute["value"]))
        else:
            _find_and_replace_expressions_in_dict(attribute, visited)

    # Dictionary
    if isinstance(obj, dict):
        for key in obj.keys():
            if _is_obj_expression_dict(obj[key]):
                obj[key] = DataFactoryElement(obj[key]["value"])
                continue

            _find_and_replace_expressions_in_dict(obj[key], visited)

    # List
    if isinstance(obj, list):
        for item in obj:
            if _is_obj_expression_dict(item):
                obj[obj.index(item)] = DataFactoryElement(item["value"])
                continue

            _find_and_replace_expressions_in_dict(item, visited)


def _is_obj_expression_dict(obj: Any) -> bool:  # noqa: ANN401
    return (
        isinstance(obj, dict)
        and ("type" in obj.keys())
        and (obj["type"] == "Expression")
        and ("value" in obj.keys())
        and len(obj.keys()) == 2
    )
