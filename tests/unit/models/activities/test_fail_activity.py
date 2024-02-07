from data_factory_testing_framework.models.activities.fail_activity import FailActivity
from data_factory_testing_framework.models.data_factory_element import DataFactoryElement
from data_factory_testing_framework.state import PipelineRunState
from data_factory_testing_framework.state.dependency_condition import DependencyCondition


def test_fail_activity_evaluates_to_failed_result() -> None:
    # Arrange
    fail_activity = FailActivity(
        name="FailActivity",
        typeProperties={
            "message": DataFactoryElement("@concat('Error code: ', '500')"),
            "errorCode": "500",
        },
        depends_on=[],
    )

    state = PipelineRunState()

    # Act
    activity = fail_activity.evaluate(state)

    # Assert
    assert activity is not None
    assert activity.name == "FailActivity"
    assert activity.status == DependencyCondition.FAILED
    assert activity.type_properties["message"].result == "Error code: 500"
    assert activity.type_properties["errorCode"] == "500"
