# Data Factory - Testing Framework :hammer_and_wrench:

A stand-alone test framework that allows to write unit tests for Data Factory pipelines on [Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-factory/) and [Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities?tabs=data-factory).

> The framework is currently in _Public Preview_ and is not officially supported by Microsoft.

## Features :rocket:

The framework evaluates pipeline and activity definitions which can be asserted. It does so by providing the following features:

1. Evaluate expressions by using the framework's internal expression parser. It supports all the functions and arguments that are available in the Data Factory expression language.
2. Test an activity with a specific state and assert the evaluated expressions.
3. Test a pipeline run by verifying the execution flow of activities for specific input parameters and assert the evaluated expressions of each activity.

> The framework does not support running the actual pipeline. It only gives you the ability to test the pipeline and activity definitions.

### High-level example :bulb:

Given a `WebActivity` with a `typeProperties.url` property containing the following expression:

```datafactoryexpression
@concat(pipeline().globalParameters.BaseUrl, variables('Path'))
```

A simple test to validate that the concatenation is working as expected could look like this:

```python
    # Arrange
    activity = pipeline.get_activity_by_name("webactivity_name")
    state = PipelineRunState(
        parameters=[
            RunParameter(RunParameterType.Global, "BaseUrl", "https://example.com"),
        ],
        variables=[
            PipelineRunVariable("Path", "some-path"),
        ])

    # Act
    activity.evaluate(state)

    # Assert
    assert "https://example.com/some-path" == activity.type_properties["url"].result
   ```

## Why :question:

Data Factory does not support unit testing, nor testing of pipelines locally. Having integration and e2e tests running on an actual Data Factory instance is great, but having unit tests on top of them provides additional means of quick iteration, validation and regression testing. Unit testing with the _Data Factory Testing Framework_ has the following benefits:

* Runs locally with immediate feedback
* Easier to cover a lot of different scenarios and edge cases
* Regression testing

## Concepts :books:

The following pages go deeper into different topics and concepts of the framework to help in getting you started.

### Basic :seedling:

1. [Repository setup](docs/basic/repository_setup.md)
2. [Installing and initializing the framework](docs/basic/installing_and_initializing_framework.md)
3. [State](docs/basic/state.md)
4. [Activity testing](docs/basic/activity_testing.md)
5. [Pipeline testing](docs/basic/pipeline_testing.md)

> If you are a not that experienced with Python, you can follow the [Getting started](docs/basic/getting_started.md) guide to get started with the framework.

### Advanced :microscope:

1. [Debugging your activities and pipelines](docs/advanced/debugging.md)
2. [Development workflow](docs/advanced/development_workflow.md)
3. [Overriding expression functions](docs/advanced/overriding_expression_functions.md)
4. [Framework internals](docs/advanced/framework_internals.md)

## Examples :memo:

More advanced examples demonstrating the capabilities of the framework:

Fabric:

1. [Batch job example](examples/fabric/batch_job/README.md)

Azure Data Factory:

1. [Copy blobs example](examples/data_factory/copy_blobs/README.md)
2. [Batch job example](examples/data_factory/batch_job/README.md)

## Limitations :warning:

The framework has the following limitations at the moment:

1. The framework reimplements the Data Factory expression language in Python. This means that it might not be 100% accurate with the actual Data Factory language, especially when it comes to xml functions.
2. The framework does not support automatic type conversion of arguments passed to functions in expressions.

> These limitations are top priority to be resolved in the future.

## Contributing :handshake:

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit <https://cla.opensource.microsoft.com>.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks :tm:

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
