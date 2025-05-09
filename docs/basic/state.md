# State

The framework provides a `PipelineRunState` class that represents the state of a pipeline run. It's used to evaluate how an activity behaves for a given a specific input.

## Interface

The constructor of the `PipelineRunState` class has the following properties:

* `parameters`: A list of `RunParameter` instances representing the input parameters of the pipeline run.
* `variables`: A list of `PipelineRunVariable` instances representing the variables of the pipeline run.
* `activity_results`: A list of activity results that can be used to simulate the output of activities in the pipeline run.
* `iteration_item`: An optional iteration item that can be used to simulate the iteration item of a ForEach activity.

The `PipelineRunState` class has the following methods:

* `add_activity_result`: Adds a result for an activity to the state. This is useful if an expression in an activity references another activities output, like: `@activity('another_activity_name').output.some_field`.
* `set_iteration_item`: Sets the iteration item of the state. This is useful if an expression in an activity references the iteration item of a ForEach activity, like: `@item().JobId`.

## Usage

### Parameters and variables

In the scenario where an activity has an expression that references a global parameter called `BaseUrl` and a variable called `JobName`, the `PipelineRunState` can be used to simulate the evaluation of the expression.

```python
state = PipelineRunState(
    parameters=[
        RunParameter(RunParameterType.Global, "BaseUrl", "https://example.com"),
    ],
    variables=[
        PipelineRunVariable("JobName", "Job-123"),
    ])
```

The following `RunParameterType` values are available:

* `RunParameterType.Parameter` to set a pipeline parameter: `@pipeline().parameters.<parameter_name>`
* `RunParameterType.Global` to set a global parameter: `@pipeline().globalParameters.<global_parameter_name>`
* `RunParameterType.System` to set a system parameter: `@pipeline().<system_parameter_name>`
* `RunParameterType.Dataset` to set a dataset: `@dataset().<dataset_name>`
* `RunParameterType.LinkedService` to set a linked service: `@linkedService().<linked_service_name>`
* `RunParameterType.LibraryVariables` to set a library variable: `@pipeline().libraryVariables.<variable_name>`

### Activity results

In the scenario where an activity has an expression that references the output of another activity `activity('another_activity_name').output.some_field`, the `PipelineRunState` can be used to configure the output of the `another_activity_name` activity.

Via the constructor:

```python
state = PipelineRunState(
    activity_results=[
        ActivityResult("another_activity_name", DependencyCondition.SUCCEEDED, {"some_field": "some_value!"}),
    ])
```

Via a method on an existing state:

```python
state.add_activity_result("another_activity_name", DependencyCondition.SUCCEEDED, {"some_field": "some_value!"})
```

### Iteration item

In the scenario where an activity has an expression that references the iteration item of a ForEach activity `@item().JobId`, the `PipelineRunState` can be used to configure the iteration item.

```python
state.set_iteration_item({"JobId": "123"})
```
