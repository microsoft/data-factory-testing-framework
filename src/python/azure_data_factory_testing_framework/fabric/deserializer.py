import json
from typing import Any

from azure_data_factory_testing_framework.fabric.models.activities.fabric_activity import FabricActivity
from azure_data_factory_testing_framework.fabric.models.activities.fabric_execute_pipeline_activity import (
    FabricExecutePipelineActivity,
)
from azure_data_factory_testing_framework.fabric.models.activities.fabric_for_each_activity import FabricForEachActivity
from azure_data_factory_testing_framework.fabric.models.activities.fabric_if_condition_activity import (
    FabricIfConditionActivity,
)
from azure_data_factory_testing_framework.fabric.models.activities.fabric_set_variable_activity import (
    FabricSetVariableActivity,
)
from azure_data_factory_testing_framework.fabric.models.activities.fabric_until_activity import FabricUntilActivity
from azure_data_factory_testing_framework.fabric.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.fabric.models.fabric_pipeline import FabricPipeline


def parse_pipeline_from_json(json_str: str) -> FabricPipeline:
    json_data = json.loads(json_str)

    properties = json_data.get("properties", {})
    parameters = properties.get("parameters", {})
    variables = properties.get("variables", {})
    activities_data = properties.get("activities", [])
    annotations = properties.get("annotations", [])

    activities = []
    for activity_data in activities_data:
        if activity_data["type"] == "SetVariable":
            activities.append(FabricSetVariableActivity(**activity_data))
        elif activity_data["type"] == "Until":
            activities.append(FabricUntilActivity(**activity_data))
        elif activity_data["type"] == "ExecutePipeline":
            activities.append(FabricExecutePipelineActivity(**activity_data))
        elif activity_data["type"] == "IfCondition":
            activities.append(FabricIfConditionActivity(**activity_data))
        elif activity_data["type"] == "ForEach":
            activities.append(FabricForEachActivity(**activity_data))
        else:
            activities.append(FabricActivity(**activity_data))

    # TODO: Load pipeline_name from item.metadata.json
    pipeline = FabricPipeline("batch_job", parameters, variables, activities, annotations)

    _find_and_replace_expressions_in_dict(pipeline)

    return pipeline


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
