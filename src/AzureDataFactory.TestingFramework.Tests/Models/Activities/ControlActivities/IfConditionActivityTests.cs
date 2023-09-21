// Copyright (c) Microsoft Corporation.

using Azure.Core.Expressions.DataFactory;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models.Activities.ControlActivities;

public class IfConditionActivityTests
{
    [Fact]
    public void WhenEvaluated_ShouldEvaluateExpression()
    {
        // Arrange
        var activity = new IfConditionActivity("IfConditionActivity",
            new DataFactoryExpression(DataFactoryExpressionType.Expression, "@equals(1, 1)"));

        // Act
        activity.Evaluate(new PipelineRunState());

        // Assert
        Assert.True(activity.EvaluatedExpression);
    }

    [Theory]
    [InlineData(true, "setVariableActivity1")]
    [InlineData(false, "setVariableActivity2")]
    public void WhenEvaluated_ShouldEvaluateCorrectChildActivities(bool expressionOutcome, string expectedActivityName)
    {
        // Arrange
        var expression = expressionOutcome ? "@equals(1, 1)" : "@equals(1, 2)";
        var activity = new IfConditionActivity("IfConditionActivity",
            new DataFactoryExpression(DataFactoryExpressionType.Expression, expression))
        {
            IfTrueActivities = { new SetVariableActivity("setVariableActivity1") { VariableName = "variable", Value = "dummy" } },
            IfFalseActivities = { new SetVariableActivity("setVariableActivity2") { VariableName = "variable", Value = "dummy" } }
        };
        var state = new PipelineRunState();
        state.Variables.Add(new PipelineRunVariable<string>("variable", string.Empty));
        activity.Evaluate(state);

        // Act
        var childActivities = activity.EvaluateChildActivities(state).ToList();

        // Assert
        Assert.Single(childActivities);
        Assert.Equal(expectedActivityName, childActivities.First().Name);
    }
}