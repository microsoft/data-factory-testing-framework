# Overriding expression functions

The framework supports mocking non-deterministic expression functions, such as as `rand` or `utcnow` by
providing mock results for them. This can be useful for non-deterministic functions or for testing purposes.

## Providing mock results for Expression Functions

You can provide mock results in two ways:

1. **Using the `data_factory_testing_framework.mock_helpers` module**: This provides the recommended and most convenient way to mock functions by passing either a single value or a list of values that will be returned in sequence.
2. **Using the `Mock` class directly**: This allows to create a mock object directly and set its return value.

When providing mock results, you can specify a **single value** or a **list of values**. If you provide a list, the mock will return the values in sequence for each call to the function similar to how `unittest.mock` works.

### Single Value Mocking

Assume a simple data pipeline that uses the `utcnow` function to set a variable using the SetVariable activity.

The example can be found in the `examples/fabric/mock_example` folder.

```python

# Arrange
fabric_folder = Path(request.fspath.dirname, "fabric")
test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=fabric_folder)
pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

# Mock the utcnow function to return a fixed datetime:
utcnow_mock = mock_utcnow("1990-05-12T10:30:00Z")

# Act
activities = test_framework.evaluate_pipeline(
    pipeline=pipeline,
    parameters=[]
    mocks=[utcnow_mock]
)

# Assert
activity = next(activities)
assert activity.type_properties["value"].result == ["1990-05-12T10:30:00Z", "1990-05-12T10:30:00Z"]
```

### List of Values Mocking

You can also provide a list of values to be returned in sequence. This is useful when you want to simulate different results for each call to the function.

```python
def test_mock_utcnow_example(request: pytest.FixtureRequest) -> None:
# Arrange
fabric_folder = Path(request.fspath.dirname, "fabric")
test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=fabric_folder)
pipeline = test_framework.get_pipeline_by_name("ExamplePipeline")

# Create a global mock for utcnow
utcnow_mock = mock_utcnow(
    [
        "1980-05-12T10:30:00Z",
        "1990-05-12T10:30:00Z",
    ]
)

# Act
activities = test_framework.evaluate_pipeline(
    pipeline,
    parameters=[],
    mocks=[utcnow_mock],
)

# Assert
activity = next(activities)
assert activity.type_properties["value"].result == ["1980-05-12T10:30:00Z", "1990-05-12T10:30:00Z"]

# Assert that there are no more activities
with pytest.raises(StopIteration):
    next(activities)
```

If the values are exhausted an error will be raised. This is similar to how `unittest.mock` works.


## Scope of Mocked Functions

By default, the mocked result apply to all pipelines, activties, and type properties in the current test run (i.e., when the the framework evaluates the pipline or activity).
You can also specify a scope which allows you to limit the mocked result to a specific pipeline, activity, or type property to test more specific scenarios.

```python

# TODO: Add example code for mocking expression functions

```
