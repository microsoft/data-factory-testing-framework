# Activity testing

The framework provides a way to test activities in isolation. This is useful for testing the behavior of an activity without executing the entire pipeline.

Make sure to have initialized the framework before writing tests. See [Installing and initializing the framework](installing-and-initializing-framework.md) for more information.

Once the `TestFramework` instance is created, tests can be written for the activities. A test always follows the Arrange-Act-Assert pattern:

1. **Arrange**: Get a reference to the activity to be tested and create a `PipelineRunState` instance with the input parameters and variables of the scenario that is being evaluated.
2. **Act**: Call the `evaluate` method on the activity with the `PipelineRunState` instance. The framework will find all expressions in the activity and evaluate them using the provided state.
3. **Assert**: Verify that the output of the activity matches the expected result.

The framework automatically detects expressions and put them in a `DataFactoryElement` object. This object has a `value` property that contains the evaluated value of the expression. The `value` property can be used to assert the outcome.

## Arrange-Act-Assert

The following pipeline example is used to demonstrate how each steps of the arrange-act-assert pattern can be implemented for a single activity.

```json
{
    "name": "trigger_job_pipeline",
    "parameters": {
        "JobId": {
          "type": "String"
        }
    },
    "variables": {
        "JobName": "Job-123"
    },
    "activities": [
      {
        "name": "Trigger job",
        "type": "WebActivity",
        "typeProperties": {
          "url": {
            "type": "Expression",
            "value": "@concat(pipeline().globalParameters.BaseUrl, '/jobs')"
          },
          "method": {
            "value": "POST"
          },
          "body": {
            "type": "Expression",
            "value": {
              "JobId": "@pipeline().parameters.JobId",
              "JobName": "@variables('JobName')",
              "Version": "@activity('Get version').output.Version"
            }
          }
        }
      }
  ]
}
```

Let's write a test for validating correct evaluation of the `url` property.

## Arrange

Get a reference to the activity to be tested using the `get_activity_by_name` method on the `Pipeline` instance.

```python
pipeline = test_framework.get_pipeline_by_name("trigger_job_pipeline")
activity = pipeline.get_activity_by_name("Trigger job")
```

Create a `PipelineRunState` instance with the input used in the `url` expression, so a globalParameter `BaseUrl` and a variable `JobName`.

```python
state = PipelineRunState(
    parameters=[
        RunParameter(RunParameterType.Global, "BaseUrl", "https://example.com"),
    ],
    variables=[
        PipelineRunVariable("JobName", "Job-123"),
    ])
```

> See [State](state.md) for a detailed explanation on how to use the `PipelineRunState` class.

## Act

Call the `evaluate` method on the `activity` with the `PipelineRunState` instance. This evaluates all expressions in the activity using the provided state and store the result in a `value` property.

```python
activity.evaluate(state)
```

The `evaluate` method might throw an exception if the expression is invalid or if the expression is missing required parameters, variables or activity outputs. Make sure to supply the required properties in the state.

## Assert

Verify that the output of the activity matches the expected result.

```python
assert "https://example.com/jobs" == activity.type_properties["url"].result
```

## Control activities

For testing control activities like `IfCondition`, `ForEach`, `Switch` and `Until`, it is useful to validate that the condition expression is evaluating correctly.  Make sure to use type hints to know the available properties of the control activity.

### Example

Considering that the `IfCondition` expression looks like: `@equals(pipeline().parameters.JobId, '123')`, an example is provided for that particular expression as follow:

```python
# Arrange
activity: IfConditionActivity = pipeline.get_activity_by_name("If condition")
state = PipelineRunState(
    parameters=[
        RunParameter(RunParameterType.Pipeline, "JobId", "123"),
    ],
)

# Act
activity.evaluate(state)

# Assert
assert activity.expression.result == True
```

### Testing child activities

To test the child activities of a control activity, firstly the control activity must be located, followed by the identification of its child activities. The testing procedure for the child activities is outlined in the previous section.

```python
# Arrange
activity: IfConditionActivity = pipeline.get_activity_by_name("If condition")
child_activity = activity.if_true_activities[0]  # Or loop through them by name
```

To evaluate the condition of a control activity in combination with the child activities, then write a pipeline test as described in [Pipeline testing](pipeline_testing.md).
