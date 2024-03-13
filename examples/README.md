
# Data Factory - Using the Testing Framework

To use the Testing Framework, is enough to import the published package resulting from the development
in the current repo.
The package is located in src/data_factory_testing_framework.

## Getting started with writing tests

### Running without a Dev Container

1. Set up an empty Python project with your favorite testing library
2. To use the Testing Framework, install the data-factory-testing-framework package from PyPI via your preferred package
    manager:
   * Pip: `pip install data-factory-testing-framework`
   * Poetry: `poetry add data-factory-testing-framework`
3. Start writting tests

### Running within a Dev Container

#### Pre-requirements using Dev Containers

To use a Dev Container, you need to have the following software in addition to the previous pre-requisites:

* Docker
* Visual Studio Code Remote Development Extension Pack

In order to open the project in a container follow the following steps:

* Open Visual Studio Code and clone the repository.
* Hit Control-Shift-P to open the command palette and type Dev Containers: Open Folder in Container ...
* When prompted, select the *examples* directory of the Project
* Wait for the container to build, check the logs for more information.

When the container successfully starts you can start writing your data factory pipeline tests.

## Features - Examples

The samples seen below is the *only* code that you need to write! The framework will take care of the rest.

1. Evaluate activities (e.g. a WebActivity that calls Azure Batch API)

    ```python
    # Arrange
    activity: Activity = pipeline.get_activity_by_name("Trigger Azure Batch Job")
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Global, "BaseUrl", "https://example.com"),
            RunParameter(RunParameterType.Pipeline, "JobId", "123"),
        ],
        variables=[
            PipelineRunVariable("JobName", "Job-123"),
        ],
        activity_results=[
            ActivityResult("Get version", DependencyCondition.SUCCEEDED, {"Version": "version1"}),
        ])

    # Act
    activity.evaluate(state)

    # Assert
    assert "https://example.com/jobs" == activity.type_properties["url"].result
    assert "POST" == activity.type_properties["method"].result
    body = activity.type_properties["body"].get_json_value()
    assert "123" == body["JobId"]
    assert "Job-123" == body["JobName"]
    assert "version1" == body["Version"]
   ```

2. Evaluate Pipelines and test the flow of activities given a specific input

    ```python
    # Arrange
    pipeline: PipelineResource = test_framework.get_pipeline_by_name("batch_job")

    # Runs the pipeline with the provided parameters
    activities = test_framework.evaluate_pipeline(pipeline, [
        RunParameter(RunParameterType.Pipeline, "JobId", "123"),
        RunParameter(RunParameterType.Pipeline, "ContainerName", "test-container"),
        RunParameter(RunParameterType.Global, "BaseUrl", "https://example.com"),
    ])

    set_variable_activity: Activity = next(activities)
    assert set_variable_activity is not None
    assert "Set JobName" == set_variable_activity.name
    assert "JobName" == activity.type_properties["variableName"]
    assert "Job-123" == activity.type_properties["value"].result

    get_version_activity = next(activities)
    assert get_version_activity is not None
    assert "Get version" == get_version_activity.name
    assert "https://example.com/version" == get_version_activity.type_properties["url"].result
    assert "GET" == get_version_activity.type_properties["method"]
    get_version_activity.set_result(DependencyCondition.Succeeded,{"Version": "version1"})

    create_batch_activity = next(activities)
    assert create_batch_activity is not None
    assert "Trigger Azure Batch Job" == create_batch_activity.name
    assert "https://example.com/jobs" == create_batch_activity.type_properties["url"].result
    assert "POST" == create_batch_activity.type_properties["method"]
    body = create_batch_activity.type_properties["body"].get_json_value()
    assert "123" == body["JobId"]
    assert "Job-123" == body["JobName"]
    assert "version1" == body["Version"]

    with pytest.raises(StopIteration):
        next(activities)
    ```

> See examples folder for more samples
