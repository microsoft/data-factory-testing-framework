import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType


def test_batch_job_pipeline(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory, root_folder_path=request.fspath.dirname
    )
    pipeline = test_framework.get_pipeline_by_name("xpath_example_08_a")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [],
    )

    # Assert
    activity = next(activities)
    assert activity.name == "Set XML String"

    activity = next(activities)
    assert activity.name == "Set xpath"

    activity = next(activities)
    assert activity.name == "Example as string"

    activity = next(activities)

    xml_array = activity.result

    assert isinstance(xml_array, list)

    # assert len(xml_array) == 1

    # assert xml_array[0] == "<location xmlns="https://contoso.com">Paris</location>"
    # # implies the object is a str, but in facts is xml instance
    # assert xml_array[0] == XmlObject("<location xmlns="https://contoso.com">Paris</location>")
    # xml = XmlObject()
    # xml.vaue = "<location xmlns="https://contoso.com">Paris</location>"

    # assert xml_array[0].value ==

    # assert xml_array[0] == '{"$content-type": "application/xml;charset=utf-8","$content": "PGxvY2F0aW9uIHhtbG5zPSJodHRwczovL2NvbnRvc28uY29tIj5QYXJpczwvbG9jYXRpb24+"}'
