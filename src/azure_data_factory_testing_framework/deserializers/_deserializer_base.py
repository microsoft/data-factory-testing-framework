from azure_data_factory_testing_framework.deserializers.shared._activity_deserializer import (
    _get_activity_from_activity_data,
)
from azure_data_factory_testing_framework.deserializers.shared._data_factory_element_replacer import (
    _find_and_replace_expressions_in_dict,
)
from azure_data_factory_testing_framework.models.pipeline import Pipeline


def _parse_pipeline_from_json(name: str, json_data: dict) -> Pipeline:
    properties = json_data.get("properties", {})
    activities = properties.get("activities", [])

    for activity_data in activities:
        activities[activities.index(activity_data)] = _get_activity_from_activity_data(activity_data)

    pipeline = Pipeline(name, **properties)

    _find_and_replace_expressions_in_dict(pipeline)

    return pipeline
