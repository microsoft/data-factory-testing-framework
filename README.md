# Data Factory - Unit Testing Framework

A unit test framework that allows you to write unit and functional tests for Data Factory pipelines against the git integrated json resource files.

Supporting currently:
* [Fabric Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/)
* [Azure Data Factory v2](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities?tabs=data-factory)

Planned:
* [Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities?context=%2Fazure%2Fsynapse-analytics%2Fcontext%2Fcontext&tabs=data-factory/)


## Disclaimer

This unit test framework is not officially supported. It is currently in experimental state and has not been tested with every single data factory resource. It should support all activities out-of-the-box, but has not been thoroughly tested, please report any issues in the issues section and include an example of the pipeline that is not working as expected.

If there's a lot of interest in this framework, then we will continue to improve it and move it to a production ready state. 

## Features

Goal: Validate that the evaluated pipeline configuration with its expressions are behaving as expected on runtime.

1. Evaluate expressions with their functions and arguments instantly by using the framework's internal expression parser.
2. Test a pipeline or activity against any state to assert expected outcome. State can be configured with pipeline parameters, global parameters, variables and activity outputs.
3. Simulate a pipeline run and evaluate the execution flow and outcome of each activity.
4. Dynamically supports all activity types with all their attributes.

> Pipelines and activities are not executed on any Data Factory environment, but the evaluation of the pipeline configuration is validated locally. This is different from the "validation" functionality present in the UI, which only validates the syntax of the pipeline configuration.


## Why

Data Factory does not support unit testing out of the box. The only way to validate your changes is through manual testing or running e2e tests against a deployed data factory. These tests are great to have, but miss the following benefits that unit tests, like using this unit test framework, provides:

* Shift left with immediate feedback on changes - Evaluate any individual data factory resource (pipelines, activities, triggers, datasets, linkedServices etc..), including (complex) expressions
* Allows testing individual resources (e.g. activity) for many different input values to cover more scenarios.
* Less issues in production - due to the fast nature of writing and running unit tests, you will write more tests in less time and therefore have a higher test coverage. This means more confidence in new changes, less risks in breaking existing features (regression tests) and thus far less issues in production.

> Even though Data Factory is UI-driven and writing unit tests might not be in the nature of it. How can you be confident that your changes will work as expected, and existing pipelines will not break, without writing unit tests?

## Getting started

1. Set up an empty Python project with your favorite testing library
2. Install the package using your preferred package manager:
   * Pip: `pip install azure-data-factory-testing-framework`
   * Poetry: `poetry add azure-data-factory-testing-framework`
3. Start writing tests

## Features - Examples

The samples seen below is the _only_ code that you need to write! The framework will take care of the rest. 

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
        ])
    state.add_activity_result("Get version", DependencyCondition.SUCCEEDED, {"Version": "version1"})

    # Act
    activity.evaluate(state)

    # Assert
    assert "https://example.com/jobs" == activity.type_properties["url"].value
    assert "POST" == activity.type_properties["method"].value
    assert "{ \n    \"JobId\": \"123\",\n    \"JobName\": \"Job-123\",\n    \"Version\": \"version1\",\n}" == activity.type_properties["body"].value
    ```
   
2. Evaluate Pipelines and test the flow of activities given a specific input

    ```python
    # Arrange
    pipeline: PipelineResource = test_framework.repository.get_pipeline_by_name("batch_job")

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
    assert "Job-123" == activity.type_properties["value"].value

    get_version_activity = next(activities)
    assert get_version_activity is not None
    assert "Get version" == get_version_activity.name
    assert "https://example.com/version" == get_version_activity.type_properties["url"].value
    assert "GET" == get_version_activity.type_properties["method"]
    get_version_activity.set_result(get_version_activity.name, DependencyCondition.Succeeded, {"Version": "version1"})

    create_batch_activity = next(activities)
    assert create_batch_activity is not None
    assert "Trigger Azure Batch Job" == create_batch_activity.name
    assert "https://example.com/jobs" == create_batch_activity.type_properties["url"].value
    assert "POST" == create_batch_activity.type_properties["method"]
    assert "{ \n    \"JobId\": \"123\",\n    \"JobName\": \"Job-123\",\n    \"Version\": \"version1\",\n}" == create_batch_activity.type_properties["body"].value

    with pytest.raises(StopIteration):
        next(activities)
    ```
   
> See Examples folder for more samples

## Registering missing expression functions

As the framework is interpreting expressions containing functions, these functions need to be implemented in Python. The goal is to start supporting more and more functions, but if a function is not supported, then the following code can be used to register a missing function:

```python
   FunctionsRepository.register("concat", lambda arguments: "".join(arguments))
   FunctionsRepository.register("trim", lambda text, trim_argument: text.strip(trim_argument[0]))
``` 

On runtime when evaluating expressions, the framework will try to find a matching function and assert the expected amount of arguments are supplied. If no matching function is found, then an exception will be thrown.

> Feel free to add a pull request with your own custom functions, so that they can be added to the framework and enjoyed by everyone.

## Tips

1. After parsing a data factory resource file, you can use the debugger to easily discover which classes are actually initialized so that you can cast them to the correct type.

## Recommended development workflow for Azure Data Factory v2

* Use ADF Git integration
* Use UI to create feature branch, build initial pipeline and save to feature branch
* Pull feature branch locally
* Start writing tests unit and functional tests, run them locally for immediate feedback and fix bugs
* Push changes to feature branch
* Test the new features manually through the UI in sandbox environment
* Create PR, which will run the tests in the CI pipeline
* Approve PR
* Merge to main and start deploying to dev/test/prd environments
* Run e2e tests after each deployment to validate all happy flows work on that specific environment

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.




