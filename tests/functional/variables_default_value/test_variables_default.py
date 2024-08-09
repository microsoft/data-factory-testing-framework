import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType


def test_string_default_variables(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory, root_folder_path=request.fspath.dirname
    )
    pipeline = test_framework.get_pipeline_by_name("default_variables")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [],
    )

    # Assert
    activity = next(activities)
    assert activity.name == "Set outputStringVar"
    assert activity.type_properties["value"][0]["key"] == "outputStringVar"
    assert activity.type_properties["value"][0]["value"].result == "is not null: "

    activity = next(activities)
    assert activity.name == "Set outputIntVar"
    assert activity.type_properties["value"][0]["key"] == "outputIntVar"
    assert activity.type_properties["value"][0]["value"].result == "is not null: 0"

    activity = next(activities)
    assert activity.name == "Set outputBoolVar"
    assert activity.type_properties["value"][0]["key"] == "outputBoolVar"
    assert activity.type_properties["value"][0]["value"].result == "is not null: False"

    activity = next(activities)
    assert activity.name == "Set outputArrayVar"
    assert activity.type_properties["value"][0]["key"] == "outputArrayVar"
    assert activity.type_properties["value"][0]["value"].result == "is not null: []"

    with pytest.raises(StopIteration):
        next(activities)
