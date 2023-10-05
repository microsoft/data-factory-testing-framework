// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Azure.Core.Expressions.DataFactory;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models.Activities.ControlActivities;

public class ForEachActivityTests
{
    [Fact]
    public void WhenEvaluateChildActivities_ThenShouldReturnTheActivityWithItemExpressionEvaluated()
    {
        // Arrange
        var testFramework = new TestFramework();
        var forEachActivity = new ForEachActivity("ForEachActivity",
            new DataFactoryExpression(DataFactoryExpressionType.Expression, "@split('a,b,c', ',')"),
            new List<PipelineActivity>()
            {
                new SetVariableActivity("setVariable")
                {
                    VariableName = "variable",
                    Value = new DataFactoryElement<string>("item()", DataFactoryElementKind.Expression)
                }
            });
        var state = new PipelineRunState();
        state.Variables.Add(new PipelineRunVariable<string>("variable", string.Empty));

        // Act
        forEachActivity.Evaluate(state);
        var childActivities = testFramework.Evaluate(forEachActivity, state);

        // Assert
        using var enumarator = childActivities.GetEnumerator();
        Assert.True(enumarator.MoveNext());
        var setVariableActivity = enumarator.Current as SetVariableActivity;
        Assert.NotNull(setVariableActivity);
        Assert.Equal("a", setVariableActivity.Value);
        Assert.True(enumarator.MoveNext());
        setVariableActivity = enumarator.Current as SetVariableActivity;
        Assert.NotNull(setVariableActivity);
        Assert.Equal("b", setVariableActivity.Value);
        Assert.True(enumarator.MoveNext());
        setVariableActivity = enumarator.Current as SetVariableActivity;
        Assert.NotNull(setVariableActivity);
        Assert.Equal("c", setVariableActivity.Value);
        Assert.False(enumarator.MoveNext());
    }
}