import pytest
from azure_data_factory_testing_framework.state.dependency_condition import DependencyCondition
from azure_data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


def test_execute_pipeline_activity_child_activities_executed(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path=request.fspath.dirname,
        should_evaluate_child_pipelines=True,
    )
    pipeline = test_framework.repository.get_pipeline_by_name("set_version")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [],
    )
    activity = next(activities)

    # Assert
    assert activity is not None
    assert activity.name == "GetVersion"
    assert activity.type == "WebActivity"
    assert activity.type_properties["relativeUrl"] == "version"
    assert activity.type_properties["method"] == "GET"
    assert activity.all_properties["externalReferences"]["connection"] == "6d70b649-d684-439b-a9c2-d2bb5241cd39"
    activity.set_result(DependencyCondition.Succeeded, {"version": "1.2.3"})

    activity = next(activities)
    assert activity is not None
    assert activity.name == "SetVersion"
    assert activity.type == "SetVariable"
    assert activity.type_properties["variableName"] == "version"
    assert activity.type_properties["value"].value == "1.2.3"

    with pytest.raises(StopIteration):
        next(activities)
