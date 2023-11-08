import json
import os

from data_factory_testing_framework.generated import Deserializer
from data_factory_testing_framework.models.repositories.data_factory_repository import DataFactoryRepository
from data_factory_testing_framework.models.repositories.models_repository import ModelsRepository

models_repository = ModelsRepository()
deserializer = Deserializer(models_repository.get_models())


class DataFactoryRepositoryFactory:

    @staticmethod
    def parse_from_folder(folder_path: str):
        pipelines = DataFactoryRepositoryFactory._get_data_factory_entities_by_folder_path(folder_path, "PipelineResource")
        return DataFactoryRepository(pipelines)

    @staticmethod
    def _get_data_factory_entities_by_folder_path(folder_path: str, target_class: str):
        entities = []
        files = os.listdir(folder_path)
        for file in files:
            if file.endswith(".json"):
                with (open(os.path.join(folder_path, file), 'r') as f):
                    pipeline_json = json.load(f)
                    entities.append(deserializer._deserialize(target_class, pipeline_json))

        return entities
