# Installing and initializing the framework

## Install dotnet runtime

Install the dotnet runtime (not SDK) from [here](https://dotnet.microsoft.com/en-us/download/dotnet/8.0). This is required to run some expression functions on dotnet just like in Data Factory.

## Installing the framework

The framework is available as a Python package on PyPI. You can install it using your preferred package manager: [data-factory-testing-framework](https://pypi.org/project/data-factory-testing-framework/).

## Initializing the framework

To initialize the framework, you need to create a `TestFramework` instance. This instance is the entry point to the framework and provides access to the pipeline and activity definitions. Specify the type of data factory (i.e. Fabric or DataFactory for Azure Data Factory) and pass the path to the folder containing the pipeline definitions to the `TestFramework` constructor.

```python
from data_factory_testing_framework import TestFramework

test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory,
        root_folder_path='/factory',
    )
```

The TestFramework will automatically load all the pipeline and activity definitions from the specified folder. It will make them available through the `repository` property. Pipelines can easily be retrieved by name:

```python
pipeline = test_framework.get_pipeline_by_name("batch_job")
```

Activities can be retrieved from the pipeline by name:

```python
activity = pipeline.get_activity_by_name("webactivity_name")
```

See the following pages for more information on how to write tests for activities and pipelines:

1. [Activity testing](activity_testing.md)
2. [Pipeline testing](pipeline_testing.md)
