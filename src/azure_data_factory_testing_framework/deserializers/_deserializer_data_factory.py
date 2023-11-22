import json

from azure_data_factory_testing_framework.deserializers._deserializer_base import _parse_pipeline_from_json
from azure_data_factory_testing_framework.models.pipeline import Pipeline


def parse_data_factory_pipeline_from_pipeline_json(pipeline_json: str) -> Pipeline:
    json_data = json.loads(pipeline_json)
    name = json_data["name"]
    return _parse_pipeline_from_json(name, json_data)
