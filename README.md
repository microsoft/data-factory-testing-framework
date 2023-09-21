# Azure Data Factory v2 - Unit Testing Framework

A unit test framework that allows you to write unit and functional tests for Azure Data Factory v2 against the git integrated json resource files.

## Disclaimer

This unit test framework is not officially supported. It is currently in experimental state and has not been tested with every single data factory resource. It should support all data factory resources, but has not been thoroughly tested, please report any issues in the issues section and include an example of the data factory pipeline that is not working as expected.

If there's a lot of interest in this framework, then I will continue to improve it and move it to a production ready state. 

## Features

1. Evaluate the outcome of any data factory resource result given a set of input parameters. The framework will evaluate parameters, globalParameters, variables, activityOutputs and their expressions, so that the final result can be asserted.
2. Simulate a pipeline run and evaluate the execution flow and outcome of each activity.
3. Automatically parse any data factory resource into the correct typed class (1500+ classes available).
4. Evaluate expressions, but not all functions are supported yet. You can always easily register your own custom functions.

## Why

Azure Data Factory does not support unit testing out of the box. The only way to validate your changes is through manual testing or running e2e tests against a deployed data factory. These tests are great to have, but miss the following benefits that unit tests, like using this unit test framework, provides:

* Shift left with immediate feedback on changes - Evaluate any individual data factory resource (pipelines, activities, triggers, datasets, linkedServices etc..), including (complex) expressions
* Allows testing individual resources (e.g. activity) for many different input values to cover more scenarios.
* Less issues in production - due to the fast nature of writing and running unit tests, you will write more tests in less time and therefore have a higher test coverage. This means more confidence in new changes, less risks in breaking existing features (regression tests) and thus far less issues in production.

> Even though Azure Data Factory is a UI-driven tool and writing unit tests might not be in the nature of it. How can you be confident that your changes will work as expected, and existing pipelines will not break, without writing unit tests?

## Getting started

1. Add the following nuget source to `nuget.config`: `https://nuget.pkg.github.com/arjendev/index.json`
2. Install the nuget package: `dotnet add package AzureDataFactory.TestingFramework --prerelease`
3. Start writing tests

## Features - Examples

The samples seen below is the _only_ code that you need to write! The framework will take care of the rest. 

1. Evaluate expressions

    ```csharp
        // Arrange 
        var expression = FunctionPart.Parse("concat('https://example.com/jobs/', '123', concat('&', 'abc'))");

        // Act
        var evaluated = expression.Evaluate();
        
        // Assert
        Assert.Equal("https://example.com/jobs/123&abc", evaluated);
    ``` 

2. Evaluate activities (e.g. a WebActivity that calls Azure Batch API), LinkedServices, Datasets and Triggers

    ```csharp
      // Arrange
      var pipeline = PipelineFactory.ParseFromFile("Example/example-pipeline.json");
      var activity = pipeline.GetActivityByName("Trigger Azure Batch Job") as WebHookActivity;
      
      _state.Parameters.Add(new RunParameter(ParameterType.Global, "BaseUrl", "https://example.com"));
      _state.Parameters.Add(new RunParameter(ParameterType.Parameter, "JobId", "123"));
      _state.Variables.Add(new PipelineRunVariable("JobName", "Job-123"));
      _state.AddActivityResult(new TestActivityResult("Get version", new
      {
        Version = "version1"
      }));
      
      // Act
      activity.Evaluate(_state);
      
      // Assert
      Assert.Equal("https://example.com/jobs", activity.Uri);
      Assert.Equal("POST", activity.Method);
      Assert.Equal("{ \n    \"JobId\": \"123\",\n    \"JobName\": \"Job-123\",\n    \"Version\": \"version1\",\n}", activity.Body);
    
    ```
   
3. Evaluate Pipelines and test the flow of activities given a specific input

    ```csharp
    var pipeline = PipelineFactory.ParseFromFile(pipelineFileName);
    Assert.Equal("example-pipeline", pipeline.Name);
    Assert.Equal(6, pipeline.Activities.Count);

    // Runs the pipeline with the provided parameters
    var activities = pipeline.EvaluateWithActivityEnumerator(new List<RunParameter>
        {
            new(ParameterType.Parameter, "JobId", "123"),
            new(ParameterType.Parameter, "ContainerName", "test-container"),
            new(ParameterType.Global, "BaseUrl", "https://example.com"),
        });

    var setVariableActivity = activities.GetNext() as SetVariableActivity;
    Assert.NotNull(setVariableActivity);
    Assert.Equal("Set JobName", setVariableActivity.Name);
    Assert.Equal("JobName", setVariableActivity.VariableName);
    Assert.Equal("Job-123", setVariableActivity.Value);

    var getVersionActivity = activities.GetNext() as WebActivity;
    Assert.NotNull(getVersionActivity);
    Assert.Equal("Get version", getVersionActivity.Name);
    Assert.Equal("https://example.com/version", getVersionActivity.Uri);
    Assert.Equal("GET", getVersionActivity.Method);
    Assert.Null(getVersionActivity.Body);
    getVersionActivity.SetResult(DependencyCondition.Succeeded, new {
        Version = "version1"
    });

    var createBatchActivity = activities.GetNext() as WebHookActivity;
    Assert.NotNull(createBatchActivity);
    Assert.Equal("Trigger Azure Batch Job", createBatchActivity.Name);
    Assert.Equal("https://example.com/jobs", createBatchActivity.Uri);
    Assert.Equal("POST", createBatchActivity.Method);
    Assert.Equal("{ \n    \"JobId\": \"123\",\n    \"JobName\": \"Job-123\",\n    \"Version\": \"version1\",\n}", createBatchActivity.Body);
    createBatchActivity.SetResult(DependencyCondition.Succeeded, "OK");
   
    Assert.Throws<ActivityEnumeratorException>(() => activities.GetNext());
    ```
   
> See AzureDataFactory.TestingFramework.Example project for more samples

## Registering missing expression functions

As the framework is interpreting expressions containing functions, these functions need to be implemented in C#. The goal is to start supporting more and more functions, but if a function is not supported, then the following code can be used to register a missing function:

```csharp
   FunctionsRepository.Register("concat", (IEnumerable<object> arguments) => string.Concat(arguments));
   FunctionsRepository.Register("trim", (string text, string trimArgument) => text.Trim(trimArgument[0]));
``` 

On runtime when evaluating expressions, the framework will try to find a matching function and assert the expected amount of arguments are supplied. If no matching function is found, then an exception will be thrown.

> Feel free to add a pull request with your own custom functions, so that they can be added to the framework and enjoyed by everyone.

## Tips

1. After parsing a data factory resource file, you can use the debugger to easily discover which classes are actually initialized so that you can cast them to the correct type.

## Recommended development workflow

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




