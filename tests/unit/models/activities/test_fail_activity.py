from data_factory_testing_framework.models import DataFactoryElement
from data_factory_testing_framework.models.activities import FailActivity
from data_factory_testing_framework.state import DependencyCondition, PipelineRunState


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
