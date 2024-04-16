from typing import List

from data_factory_testing_framework.models.activities import (
    Activity,
    AppendVariableActivity,
    ExecutePipelineActivity,
    FailActivity,
    FilterActivity,
    ForEachActivity,
    IfConditionActivity,
    SetVariableActivity,
    SwitchActivity,
    UntilActivity,
)


def _get_activity_from_activity_data(activity_data: dict) -> Activity:
    type_properties = activity_data["typeProperties"]
    if activity_data["type"] == "SetVariable":
        return SetVariableActivity(**activity_data)
    if activity_data["type"] == "AppendVariable":
        return AppendVariableActivity(**activity_data)
    elif activity_data["type"] == "Until":
        activities = _get_activity_from_activities_data(type_properties["activities"])
        return UntilActivity(activities=activities, **activity_data)
    elif activity_data["type"] == "ExecutePipeline":
        return ExecutePipelineActivity(**activity_data)
    elif activity_data["type"] == "IfCondition":
        if_true_activities = (
            _get_activity_from_activities_data(type_properties["ifTrueActivities"])
            if "ifTrueActivities" in type_properties
            else []
        )
        if_false_activities = (
            _get_activity_from_activities_data(type_properties["ifFalseActivities"])
            if "ifFalseActivities" in type_properties
            else []
        )
        return IfConditionActivity(
            if_true_activities=if_true_activities, if_false_activities=if_false_activities, **activity_data
        )
    elif activity_data["type"] == "ForEach":
        child_activities = _get_activity_from_activities_data(type_properties["activities"])
        return ForEachActivity(activities=child_activities, **activity_data)
    elif activity_data["type"] == "Switch":
        default_activities = (
            _get_activity_from_activities_data(type_properties["defaultActivities"])
            if "defaultActivities" in type_properties
            else []
        )
        cases_activities = {}
        for case in type_properties["cases"]:
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
