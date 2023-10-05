// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Azure.ResourceManager.DataFactory;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Tests.Models.Pipelines;

public class PipelineTests
{
    [Fact]
    public void WhenEvaluatingPipelineWithMissingParameters_ShouldThrowException()
    {
        // Arrange
        var testFramework = new TestFramework();
        var pipeline = new Pipeline();
        pipeline.Parameters.Add("key1", new EntityParameterSpecification(EntityParameterType.String));
        pipeline.Parameters.Add("key2", new EntityParameterSpecification(EntityParameterType.String));

        // Assert
        Assert.Throws<PipelineParameterNotProvidedException>(() => testFramework.Evaluate(pipeline, new List<IRunParameter>()).ToList());
    }

    [Fact]
    public void WhenEvaluatingPipeline_ShouldReturnActivities()
    {
        // Arrange
        var testFramework = new TestFramework();
        var pipeline = new Pipeline();
        pipeline.Parameters.Add("key1", new EntityParameterSpecification(EntityParameterType.String));

        // Act
        var activities = testFramework.EvaluateAll(pipeline, new List<IRunParameter>()
        {
            new RunParameter<string>(ParameterType.Parameter, "key1", "value1")
        });

        // Assert
        Assert.NotNull(activities);
        Assert.Empty(activities);
    }
}