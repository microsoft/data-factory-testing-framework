from typing import List

from azure_data_factory_testing_framework.models.activities.activity import Activity
from azure_data_factory_testing_framework.models.activities.append_variable_activity import AppendVariableActivity
from azure_data_factory_testing_framework.models.activities.execute_pipeline_activity import ExecutePipelineActivity
from azure_data_factory_testing_framework.models.activities.fail_activity import FailActivity
from azure_data_factory_testing_framework.models.activities.filter_activity import FilterActivity
from azure_data_factory_testing_framework.models.activities.for_each_activity import ForEachActivity
from azure_data_factory_testing_framework.models.activities.if_condition_activity import IfConditionActivity
from azure_data_factory_testing_framework.models.activities.set_variable_activity import SetVariableActivity
from azure_data_factory_testing_framework.models.activities.switch_activity import SwitchActivity
from azure_data_factory_testing_framework.models.activities.until_activity import UntilActivity


def _get_activity_from_activity_data(activity_data: dict) -> Activity:
    if activity_data["type"] == "SetVariable":
        return SetVariableActivity(**activity_data)
    if activity_data["type"] == "AppendVariable":
        return AppendVariableActivity(**activity_data)
    elif activity_data["type"] == "Until":
        activities = _get_activity_from_activities_data(activity_data["activities"])
        return UntilActivity(activities=activities, **activity_data)
    elif activity_data["type"] == "ExecutePipeline":
        return ExecutePipelineActivity(**activity_data)
    elif activity_data["type"] == "IfCondition":
        if_true_activities = _get_activity_from_activities_data(activity_data["typeProperties"]["ifTrueActivities"])
        if_false_activities = _get_activity_from_activities_data(activity_data["typeProperties"]["ifFalseActivities"])
        return IfConditionActivity(
            if_true_activities=if_true_activities, if_false_activities=if_false_activities, **activity_data
        )
    elif activity_data["type"] == "ForEach":
        child_activities = _get_activity_from_activities_data(activity_data["activities"])
        return ForEachActivity(activities=child_activities, **activity_data)
    elif activity_data["type"] == "Switch":
        default_activities = _get_activity_from_activities_data(activity_data["typeProperties"]["defaultActivities"])
        cases_activities = {}
        for case in activity_data["typeProperties"]["cases"]:
            case_value = case["value"]
            activities = case["activities"]
            cases_activities[case_value] = _get_activity_from_activities_data(activities)
        return SwitchActivity(default_activities=default_activities, cases_activities=cases_activities, **activity_data)
    elif activity_data["type"] == "Filter":
        return FilterActivity(**activity_data)
    elif activity_data["type"] == "Fail":
        return FailActivity(**activity_data)
    else:
        return Activity(**activity_data)


def _get_activity_from_activities_data(activities_data: dict) -> List[Activity]:
    activities = []
    for activity_data in activities_data:
        activities.append(_get_activity_from_activity_data(activity_data))

    return activities
