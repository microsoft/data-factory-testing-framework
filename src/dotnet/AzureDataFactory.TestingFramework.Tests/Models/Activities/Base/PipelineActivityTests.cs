// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models.Activities.Base;

public class PipelineActivityTests
{
    [Theory]
    [InlineData("Succeeded", "Succeeded", true)]
    [InlineData("Failed", "Succeeded", false)]
    [InlineData("Skipped", "Succeeded", false)]
    [InlineData("Completed", "Succeeded", false)]
    [InlineData("Failed", "Failed", true)]
    [InlineData("Skipped", "Failed", false)]
    [InlineData("Completed", "Failed", false)]
    [InlineData("Skipped", "Skipped", true)]
    [InlineData("Completed", "Skipped", false)]
    [InlineData("Completed", "Completed", true)]
    public void DependencyConditions_WhenCalled_ReturnsExpected(string requiredCondition, string actualCondition, bool expected)
    {
        // Arrange
        var pipelineActivity = new PipelineActivity("activity")
        {
            DependsOn = { new PipelineActivityDependency("otherActivity", new[] { new DependencyCondition(requiredCondition) }) }
        };
        var state = new PipelineRunState();
        state.AddActivityResult(new TestActivityResult("otherActivity", new DependencyCondition(actualCondition)));

        // Assert
        Assert.Equal(expected, pipelineActivity.AreDependencyConditionMet(state));
    }

    [Fact]
    public void EvaluateWhenNoStatusIsSet_ShouldSetStatusToSucceeded()
    {
        // Arrange
        var pipelineActivity = new PipelineActivity("activity");
        var state = new PipelineRunState();

        // Act
        pipelineActivity.Evaluate(state);

        // Assert
        Assert.Equal(DependencyCondition.Succeeded, pipelineActivity.Status);
    }
}