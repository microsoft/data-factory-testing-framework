from data_factory_testing_framework.generated import models as _models

from data_factory_testing_framework.models.activities.base import Activity


class ModelsRepository:

    def __init__(self):
        # Patch models with our custom classes
        Activity.patch_generated_models(_models)

        self.models = {k: v for k, v in _models.__dict__.items() if isinstance(v, type)}

    def get_models(self):
        return self.models