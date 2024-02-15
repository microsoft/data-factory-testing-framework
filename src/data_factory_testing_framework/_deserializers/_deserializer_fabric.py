import json

from data_factory_testing_framework._deserializers._deserializer_base import _parse_pipeline_from_json
from data_factory_testing_framework.models import Pipeline


def parse_fabric_pipeline_from_pipeline_json_files(
    pipeline_json: str, config_json: str, metadata_json: str
) -> Pipeline:
    pipeline_logical_id = config_json["logicalId"]
    pipeline_name = metadata_json["displayName"]
    pipeline_json = json.loads(pipeline_json)
    return _parse_pipeline_from_json(pipeline_logical_id, pipeline_name, pipeline_json)
