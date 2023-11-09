from data_factory_testing_framework.generated import models as _models

from data_factory_testing_framework.models.activities.base import Activity
from data_factory_testing_framework.models.activities.control_activities.control_activity import ControlActivity
from data_factory_testing_framework.models.activities.control_activities.execute_pipeline_activity import \
    ExecutePipelineActivity
from data_factory_testing_framework.models.activities.control_activities.for_each_activity import ForEachActivity
from data_factory_testing_framework.models.expression import Expression


# Patch models with our custom classes
def patch_models():
    Activity.patch_generated_models(_models)
    ExecutePipelineActivity.patch_generated_models(_models)
    ControlActivity.patch_generated_models(_models)
    ForEachActivity.patch_generated_models(_models)
    Expression.patch_generated_models(_models)