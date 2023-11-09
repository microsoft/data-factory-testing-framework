from data_factory_testing_framework.generated import models as _models

from data_factory_testing_framework.models.activities.base import Activity
from data_factory_testing_framework.models.activities.control_activities.control_activity import ControlActivity
from data_factory_testing_framework.models.activities.control_activities.execute_pipeline_activity import \
    ExecutePipelineActivity
from data_factory_testing_framework.models.activities.control_activities.for_each_activity import ForEachActivity
from data_factory_testing_framework.models.activities.control_activities.if_condition_activity import \
    IfConditionActivity
from data_factory_testing_framework.models.expression import Expression


# Patch models with our custom classes
def patch_models():
    patch_model(_models.Activity, Activity)
    patch_model(_models.ExecutePipelineActivity, ExecutePipelineActivity)
    patch_model(_models.ControlActivity, ControlActivity)
    patch_model(_models.ForEachActivity, ForEachActivity)
    patch_model(_models.Expression, Expression)
    patch_model(_models.IfConditionActivity, IfConditionActivity)


def patch_model(main_class, partial_class):
    partial_class_method_list = [attribute for attribute in dir(partial_class) if callable(getattr(partial_class, attribute)) and attribute.startswith('__') is False]
    for method_name in partial_class_method_list:
        setattr(main_class, method_name, getattr(partial_class, method_name))