// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Azure.Core.Expressions.DataFactory;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models.Activities.Base;

public class TestFrameworkTests
{
    private readonly List<PipelineActivity> _activities;
    private readonly WebActivity _webActivity;
    private readonly SetVariableActivity _setVariableActivity;
    private readonly TestFramework _testFramework;

    public TestFrameworkTests()
    {
        _testFramework = new TestFramework();
        _activities = new List<PipelineActivity>();
        _webActivity = new WebActivity("webActivity", WebActivityMethod.Get, "https://www.example.com")
        {
            DependsOn =
            {
                new PipelineActivityDependency("setVariableActivity", new[] { DependencyCondition.Succeeded })
            }
        };
        _setVariableActivity = new SetVariableActivity("setVariableActivity")
        {
            VariableName = "variable1",
            Value = "value1"
        };
        _activities.Add(_webActivity);
        _activities.Add(_setVariableActivity);
    }

    [Fact]
    public void EvaluateWithoutIterationActivities_ShouldEvaluateAccordingToDependencies()
    {
        // Act
        var state = new PipelineRunState();
        state.Variables.Add(new PipelineRunVariable<string>("variable1", string.Empty));
        var evaluatedActivities = _testFramework.Evaluate(_activities, state).ToList();

        // Assert
        Assert.NotNull(evaluatedActivities);
        Assert.Equal(2, evaluatedActivities.Count());
        Assert.Equal("setVariableActivity", evaluatedActivities.First().Name);
        Assert.Equal("webActivity", evaluatedActivities.Last().Name);
    }

    [Fact]
    public void EvaluateWithCircularDependencies_ShouldThrowActivitiesEvaluatorInvalidDependencyException()
    {
        // Arrange
        _setVariableActivity.DependsOn.Add(new PipelineActivityDependency("webActivity", new[] { DependencyCondition.Succeeded }));

        // Assert
        Assert.Throws<ActivitiesEvaluatorInvalidDependencyException>(() => _testFramework.Evaluate(_activities, new PipelineRunState()).ToList());
    }

    [Fact]
    public void EvaluateWithForeachActivities_ShouldEvaluateAccordingToDependencies()
    {
        // Arrange
        var state = new PipelineRunState();
        state.Variables.Add(new PipelineRunVariable<string>("variable1", string.Empty));
        state.Variables.Add(new PipelineRunVariable<string>("iterationItems", "item1,item2,item3"));
        var foreachActivity = new ForEachActivity("foreachActivity",
            new DataFactoryExpression(DataFactoryExpressionType.Expression, "@split(variables('iterationItems'), ',')"),
            _activities);
        _webActivity.Uri = new DataFactoryElement<string>("@concat('https://www.example.com/', item())", DataFactoryElementKind.Expression);

        // Act
        var evaluatedActivities = _testFramework.Evaluate(new List<PipelineActivity> { foreachActivity }, state);

        // Assert
        using var enumerator = evaluatedActivities.GetEnumerator();
        Assert.True(enumerator.MoveNext());
        Assert.Equal("setVariableActivity", enumerator.Current.Name);
        Assert.True(enumerator.MoveNext());
        Assert.Equal("webActivity", enumerator.Current.Name);
        Assert.Equal("https://www.example.com/item1", ((WebActivity)enumerator.Current).Uri);
        Assert.True(enumerator.MoveNext());
        Assert.Equal("setVariableActivity", enumerator.Current.Name);
        Assert.True(enumerator.MoveNext());
        Assert.Equal("webActivity", enumerator.Current.Name);
        Assert.Equal("https://www.example.com/item2", ((WebActivity)enumerator.Current).Uri);
        Assert.True(enumerator.MoveNext());
        Assert.Equal("setVariableActivity", enumerator.Current.Name);
        Assert.True(enumerator.MoveNext());
        Assert.Equal("webActivity", enumerator.Current.Name);
        Assert.Equal("https://www.example.com/item3", ((WebActivity)enumerator.Current).Uri);
        Assert.False(enumerator.MoveNext());
    }

    [Fact]
    public void EvaluateWithUntilActivities_ShouldEvaluateAccordingToDependencies()
    {
        // Arrange
        var state = new PipelineRunState();
        state.Variables.Add(new PipelineRunVariable<string>("variable1", string.Empty));
        var untilActivity = new UntilActivity("untilActivity",
            new DataFactoryExpression(DataFactoryExpressionType.Expression, "@equals(variables('variable1'), 'value1')"),
            _activities);

        // Act
        var evaluatedActivities = _testFramework.Evaluate(new List<PipelineActivity> { untilActivity }, state);

        // Assert
        using var enumerator = evaluatedActivities.GetEnumerator();
        Assert.True(enumerator.MoveNext());
        Assert.Equal("setVariableActivity", enumerator.Current.Name);
        Assert.True(enumerator.MoveNext());
        Assert.Equal("webActivity", enumerator.Current.Name);
        Assert.False(enumerator.MoveNext());
    }
}