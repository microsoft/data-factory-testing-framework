import json

from azure_data_factory_testing_framework.deserializers.shared._activity_deserializer import (
    _get_activity_from_activity_data,
)
from azure_data_factory_testing_framework.deserializers.shared._data_factory_element_replacer import (
    _find_and_replace_expressions_in_dict,
)
from azure_data_factory_testing_framework.models.pipeline import Pipeline


def parse_pipeline_from_json(metadata_json: str, pipeline_json: str) -> Pipeline:
    metadata_json = json.loads(metadata_json)
    pipeline_json = json.loads(pipeline_json)

    properties = pipeline_json.get("properties", {})
    activities = properties.get("activities", [])

    for activity_data in activities:
        activities[activities.index(activity_data)] = _get_activity_from_activity_data(activity_data)

    pipeline_json = Pipeline(metadata_json["displayName"], **properties)

    _find_and_replace_expressions_in_dict(pipeline_json)

    return pipeline_json
