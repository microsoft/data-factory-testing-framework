from data_factory_testing_framework._deserializers.shared._activity_deserializer import (
    _get_activity_from_activity_data,
)
from data_factory_testing_framework._deserializers.shared._data_factory_element_replacer import (
    _find_and_replace_expressions_in_dict,
)
from data_factory_testing_framework.models import Pipeline


def _parse_pipeline_from_json(pipeline_id: str, name: str, json_data: dict) -> Pipeline:
    properties = json_data.get("properties", {})
    activities = properties.get("activities", [])

    for activity_data in activities:
        activities[activities.index(activity_data)] = _get_activity_from_activity_data(activity_data)

    pipeline = Pipeline(pipeline_id, name, **properties)

    _find_and_replace_expressions_in_dict(pipeline)

    return pipeline
