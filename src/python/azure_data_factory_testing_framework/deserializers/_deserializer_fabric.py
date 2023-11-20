import json

from azure_data_factory_testing_framework.deserializers.shared._activity_deserializer import (
    _get_activity_from_activity_data,
)
from azure_data_factory_testing_framework.deserializers.shared._data_factory_element_replacer import (
    _find_and_replace_expressions_in_dict,
)
from azure_data_factory_testing_framework.models.pipeline import Pipeline


def parse_pipeline_from_json(json_str: str) -> Pipeline:
    json_data = json.loads(json_str)

    properties = json_data.get("properties", {})
    activities_data = properties.get("activities", [])

    activities = []
    for activity_data in activities_data:
        activities.append(_get_activity_from_activity_data(activity_data))

    # TODO: Load pipeline_name from item.metadata.json
    properties["activities"] = activities
    pipeline = Pipeline("batch_job", **properties)

    _find_and_replace_expressions_in_dict(pipeline)

    return pipeline
