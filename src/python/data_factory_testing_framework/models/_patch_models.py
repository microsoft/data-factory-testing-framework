from data_factory_testing_framework.generated import models as _models
from data_factory_testing_framework.models.expressions._data_factory_element import DataFactoryElement
from data_factory_testing_framework.models.expressions._expression import Expression
from data_factory_testing_framework.models.activities.base.activity import Activity
from data_factory_testing_framework.models.activities.control_activities.execute_pipeline_activity import (
    ExecutePipelineActivity,
)
from data_factory_testing_framework.models.activities.control_activities.for_each_activity import ForEachActivity
from data_factory_testing_framework.models.activities.control_activities.if_condition_activity import (
    IfConditionActivity,
)
from data_factory_testing_framework.models.activities.control_activities.until_activity import UntilActivity
from data_factory_testing_framework.models.activities.set_variable_activity import SetVariableActivity
from data_factory_testing_framework.models.pipelines.pipeline_resource import PipelineResource


# Patch models with our custom classes
def patch_models() -> None:
    patch_model(_models.Activity, Activity)
    patch_model(_models.ExecutePipelineActivity, ExecutePipelineActivity)
    patch_model(_models.ForEachActivity, ForEachActivity)
    patch_model(_models.Expression, Expression)
    patch_model(_models.IfConditionActivity, IfConditionActivity)
    patch_model(_models.UntilActivity, UntilActivity)
    patch_model(_models.SetVariableActivity, SetVariableActivity)
    patch_model(_models.PipelineResource, PipelineResource)
    patch_model(_models.DataFactoryElement, DataFactoryElement)


def patch_model(main_class: type, partial_class: type) -> None:
    partial_class_method_list = [
        attribute
        for attribute in dir(partial_class)
        if callable(getattr(partial_class, attribute)) and attribute.startswith("__") is False
    ]
    for method_name in partial_class_method_list:
        setattr(main_class, method_name, getattr(partial_class, method_name))
