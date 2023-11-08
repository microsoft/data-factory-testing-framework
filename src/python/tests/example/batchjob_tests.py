from data_factory_testing_framework.generated.models import WebActivity, DependencyCondition
from data_factory_testing_framework.models.test_framework import TestFramework


def test_batch_job_pipeline():
    # Arrange
    test_framework = TestFramework("pipelines")
    pipeline = test_framework.repository.get_pipeline_by_name("batch_job")
    web_activity: WebActivity = pipeline.activities[0]

    # Act
    result = test_framework.evaluate(web_activity)

    # Assert
    assert web_activity.body.value == "test2"
    assert result == DependencyCondition.Succeeded
