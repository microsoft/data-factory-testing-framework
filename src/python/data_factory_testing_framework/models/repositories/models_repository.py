from data_factory_testing_framework.generated import models as _models

from data_factory_testing_framework.models.activities.base import Activity
from data_factory_testing_framework.models.activities.control_activities.control_activity import ControlActivity
from data_factory_testing_framework.models.activities.control_activities.execute_pipeline_activity import \
    ExecutePipelineActivity


class ModelsRepository:

    def __init__(self):
        # Patch models with our custom classes
        Activity.patch_generated_models(_models)
        ControlActivity.patch_generated_models(_models)
        ExecutePipelineActivity.patch_generated_models(_models)

        self.models = {k: v for k, v in _models.__dict__.items() if isinstance(v, type)}

    def get_models(self):
        return self.models
