import json

from data_factory_testing_framework._deserializers._deserializer_base import _parse_pipeline_from_json
from data_factory_testing_framework.models import Pipeline


def parse_data_factory_pipeline_from_pipeline_json(pipeline_json: str) -> Pipeline:
    json_data = json.loads(pipeline_json)
    name = json_data["name"]

    # The name is used as the id, because this is how Azure Data Factory uniquely identifies pipelines
    return _parse_pipeline_from_json(name, name, json_data)
