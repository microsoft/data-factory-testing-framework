// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Functional.Pipelines.Child;

public class ChildPipelineTests
{
    [Fact]
    public void WhenExecutePipelineActivityIsCalled_ThenChildPipelineActivitiesAreExecuted()
    {
        // Arrange
        var testFramework = new TestFramework(dataFactoryFolderPath: "Functional/Pipelines/Child", shouldEvaluateChildPipelines: true);
        var pipeline = testFramework.Repository.GetPipelineByName("main");

        // Act
        var activities = testFramework.Evaluate(pipeline, new List<IRunParameter>()
        {
            new RunParameter<string>(ParameterType.Parameter, "Url", "https://example.com"),
            new RunParameter<string>(ParameterType.Parameter, "Body", "{ \"key\": \"value\" }")
        });

        // Assert
        var childWebActivity = activities.GetNext<WebActivity>();
        Assert.Equal("API Call", childWebActivity.Name);
        Assert.Equal("https://example.com", childWebActivity.Uri);
        Assert.Equal("{ \"key\": \"value\" }", childWebActivity.Body);
    }

    [Fact]
    public void WhenExecutePipelineActivityIsCalledAndIsConfiguredToEvaluateChildPipelinesAndChildPipelineIsNotKnown_ThenExceptionShouldBeThrown()
    {
        // Arrange
        var testFramework = new TestFramework(shouldEvaluateChildPipelines: true);
        var pipeline = PipelineFactory.ParseFromFile("Functional/Pipelines/Child/pipeline/main.json");

        // Act
        var exception = Assert.Throws<PipelineNotFoundException>(() => testFramework.EvaluateAll(pipeline, new List<IRunParameter>()
        {
            new RunParameter<string>(ParameterType.Parameter, "Url", "https://example.com"),
            new RunParameter<string>(ParameterType.Parameter, "Body", "{ \"key\": \"value\" }")
        }));

        // Assert
        Assert.Equal("Pipeline with name 'child' was not found in the repository. Make sure to load the repository before evaluating pipelines.", exception.Message);
    }
}
