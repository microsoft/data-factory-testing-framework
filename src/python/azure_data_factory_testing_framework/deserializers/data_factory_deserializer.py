import json
from typing import Any, List

from azure_data_factory_testing_framework.models.activities.activity import Activity
from azure_data_factory_testing_framework.models.activities.execute_pipeline_activity import (
    ExecutePipelineActivity,
)
from azure_data_factory_testing_framework.models.activities.for_each_activity import ForEachActivity
from azure_data_factory_testing_framework.models.activities.if_condition_activity import (
    IfConditionActivity,
)
from azure_data_factory_testing_framework.models.activities.set_variable_activity import (
    SetVariableActivity,
)
from azure_data_factory_testing_framework.models.activities.until_activity import UntilActivity
from azure_data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from azure_data_factory_testing_framework.models.pipeline import Pipeline


def parse_pipeline_from_json(json_str: str) -> Pipeline:
    json_data = json.loads(json_str)

    name = json_data["name"]
    properties = json_data.get("properties", {})
    parameters = properties.get("parameters", {})
    variables = properties.get("variables", {})
    activities_data = properties.get("activities", [])
    annotations = properties.get("annotations", [])

    activities = []
    for activity_data in activities_data:
        activities.append(_get_activity_from_activity_data(activity_data))

    pipeline = Pipeline(name, parameters, variables, activities, annotations)

    _find_and_replace_expressions_in_dict(pipeline)

    return pipeline


def _get_activity_from_activity_data(activity_data: dict) -> Activity:
    if activity_data["type"] == "SetVariable":
        return SetVariableActivity(**activity_data)
    elif activity_data["type"] == "Until":
        activities = _get_activity_from_activities_data(activity_data["activities"])

        return UntilActivity(activities=activities, **activity_data)
    elif activity_data["type"] == "ExecutePipeline":
        return ExecutePipelineActivity(**activity_data)
    elif activity_data["type"] == "IfCondition":
        if_true_activities = _get_activity_from_activities_data(activity_data["typeProperties"]["ifTrueActivities"])
        if_false_activities = _get_activity_from_activities_data(activity_data["typeProperties"]["ifFalseActivities"])
        return IfConditionActivity(
            if_true_activities=if_true_activities, if_false_activities=if_false_activities, **activity_data
        )
    elif activity_data["type"] == "ForEach":
        child_activities = _get_activity_from_activities_data(activity_data["activities"])
        return ForEachActivity(activities=child_activities, **activity_data)
    else:
        return Activity(**activity_data)


def _get_activity_from_activities_data(activities_data: dict) -> List[Activity]:
    activities = []
    for activity_data in activities_data:
        activities.append(_get_activity_from_activity_data(activity_data))

    return activities


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
