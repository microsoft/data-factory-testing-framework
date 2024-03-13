# Pipeline testing

The framework provides a way to evaluate a pipeline and validate the execution flow of each activity and ensure that the outcome of one activity is correctly passed to the next activity.

Get acquainted with the [Activity testing](activity_testing.md) page before proceeding with pipeline testing, because similar concepts are used.

Make sure to have initialized the framework before writing tests. See [Installing and initializing the framework](installing_and_initializing_framework.md) for more information.

Once the `TestFramework` instance is created,  tests can be written for the pipelines. A test always follows the Arrange-Act-Assert pattern:

1. **Arrange**: Get a reference to the pipeline to be tested
2. **Act**: Call the `evaluate_pipeline` method on the `TestFramework` instance with the pipeline and the input parameters of the scenario to be evaluated.
3. **Assert**: Request the next activity from the returned generator and verify that the output of the activity matches the expected result. Repeat until all activities have been evaluated.

## Arrange-Act-Assert

The following pipeline example is used to demonstrate how each steps of the arrange-act-assert pattern can be implemented for a pipeline.

```json
{
    "parameters": {
        "JobId": {
          "type": "String"
        }
    },
    "variables": {
        "JobName": ""
    },
    "activities": [
      {
        "name": "Set JobName",
        "type": "SetVariable",
        "typeProperties": {
          "variableName": "JobName",
          "value": {
            "type": "Expression",
            "value": "@concat('Job-', pipeline().parameters.JobId)"
          }
        }
      },
      {
        "name": "Get version of job",
        "type": "WebActivity",
        "typeProperties": {
          "url": {
            "type": "Expression",
            "value": "@concat(pipeline().globalParameters.BaseUrl, '/', variables('JobName'), '/version)"
          },
          "method": {
            "value": "GET"
          }
        },
        "dependsOn": [
          {
            "activity": "Set JobName",
            "dependencyConditions": [
              "Succeeded"
            ]
          }
        ]
      }
  ]
}
```

Let's write a test for validating the correct flow of activities, the correct setting of the variable and the correct evaluation of the `url` property.

## Arrange

Get a reference to the pipeline to be tested using the `get_pipeline_by_name` method on the `Repository` instance.

```python
pipeline = test_framework.get_pipeline_by_name("batch_job")
```

## Act

Start evaluating the pipeline with the requested parameters. The `evaluate_pipeline` method returns a generator that yields the activities in the order they are executed.

```python
activities = test_framework.evaluate_pipeline(pipeline, [
    RunParameter(RunParameterType.Pipeline, "JobId", "123"),
    RunParameter(RunParameterType.Global, "BaseUrl", "https://example.com"),
])
```

## Assert

Request the next activity from the returned generator and verify that the output of the activity matches the expected result. Repeat until all activities have been evaluated.

```python
set_variable_activity = next(activities)
assert set_variable_activity is not None
assert "Set JobName" == set_variable_activity.name
assert "Job-123" == activity.type_properties["value"].result

get_version_activity = next(activities)
assert get_version_activity is not None
assert "Get version of job" == get_version_activity.name
assert "https://example.com/Job-123/version" == get_version_activity.type_properties["url"].result
assert "GET" == get_version_activity.type_properties["method"]
```

### Activity output references

If an activity output is being referenced (e.g. `activity('Get version of job').output.version`), make sure to set the result of the activity using the `set_result` method before requesting the next activity from the generator.

```python
get_version_activity.set_result(DependencyCondition.Succeeded, { "version", "1.0.0" })
```

The `next(activities)` method might throw an exception if the expression is invalid or if a property of an expression is not (yet) available in the state. Make sure that:

1. Parameters are supplied
2. Variables are being set correctly through the `SetVariable` activity
3. Activity outputs being referenced are set through `activity.set_result` method
4. Dependency conditions are met

### Asserting end of pipeline execution

When the generator has no more activities to return, it raises a `StopIteration` exception. This is a signal that all activities have been evaluated or that no activities meet the required dependency conditions. If the pipeline is expected to be finished, it can be asserted using the `pytest.raises` context manager:

```python
with pytest.raises(StopIteration):
    next(activities)
```

## Control activities

The following activities are `ControlActivities` and are not returned by the generator: `IfCondition`, `ForEach`, `Switch` and `Until`. The conditions of these activities are automatically evaluated and the child activities are evaluated and returned based on the result of the condition.

## Execute child pipelines

Child pipelines and their activities can be included in the evaluation of the parent pipeline by setting the `should_evaluate_child_pipelines` of the `TestFramework` constructor to `True`. The framework evaluates the parameters of the`ExecutePipelineActivity` and then evaluate the child pipeline with the provided parameters. This is useful to validate that different pipelines are working well together.

```python
test_framework = TestFramework(should_evaluate_child_pipelines=True)
```
