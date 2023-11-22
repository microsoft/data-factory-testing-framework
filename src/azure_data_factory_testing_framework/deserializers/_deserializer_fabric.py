import json

from azure_data_factory_testing_framework.deserializers._deserializer_base import _parse_pipeline_from_json
from azure_data_factory_testing_framework.models.pipeline import Pipeline


def parse_fabric_pipeline_from_pipeline_json_files(metadata_json: str, pipeline_json: str) -> Pipeline:
    pipeline_name = _get_pipeline_name_from_metadata_json(metadata_json)
    pipeline_json = json.loads(pipeline_json)
    return _parse_pipeline_from_json(pipeline_name, pipeline_json)


def _get_pipeline_name_from_metadata_json(metadata_json: str) -> str:
    metadata_json = json.loads(metadata_json)
    return metadata_json["displayName"]
