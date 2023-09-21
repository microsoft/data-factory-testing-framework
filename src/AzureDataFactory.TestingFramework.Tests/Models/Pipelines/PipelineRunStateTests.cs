// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models.Pipelines;

public class PipelineRunStateTests
{
    [Fact]
    public void WhenPipelineRunStateIsInitialized_ShouldBeInitializedCorrectly()
    {
        // Act
        var state = new PipelineRunState(
            new List<IRunParameter>()
            {
                new RunParameter<string>(ParameterType.Dataset, "datasetKey", "datasetValue"),
                new RunParameter<string>(ParameterType.LinkedService, "linkedServiceKey", "linkedServiceValue"),
                new RunParameter<string>(ParameterType.Parameter, "parameterKey", "parameterValue"),
                new RunParameter<string>(ParameterType.Global, "globalParameterKey", "globalParameterValue")
            },
            new Dictionary<string, PipelineVariableSpecification>()
            {
                { "stringVariableKey", new PipelineVariableSpecification(PipelineVariableType.String) },
                { "boolVariableKey", new PipelineVariableSpecification(PipelineVariableType.Bool) }
            });

        // Assert
        Assert.NotNull(state);
        Assert.NotNull(state.Parameters);
        Assert.Equal(4, state.Parameters.Count);
        var datasetParameter = state.Parameters.Single(p => p.Name == "datasetKey");
        Assert.Equal(ParameterType.Dataset, datasetParameter.Type);

        var linkedServiceParameter = state.Parameters.Single(p => p.Name == "linkedServiceKey");
        Assert.Equal(ParameterType.LinkedService, linkedServiceParameter.Type);

        var parameterParameter = state.Parameters.Single(p => p.Name == "parameterKey");
        Assert.Equal(ParameterType.Parameter, parameterParameter.Type);

        var globalParameterParameter = state.Parameters.Single(p => p.Name == "globalParameterKey");
        Assert.Equal(ParameterType.Global, globalParameterParameter.Type);

        Assert.NotNull(state.Variables);
        Assert.Equal(2, state.Variables.Count);
        var stringVariable = state.Variables.OfType<PipelineRunVariable<string>>().Single(v => v.Name == "stringVariableKey");
        Assert.Null(stringVariable.Value);

        var boolVariable = state.Variables.OfType<PipelineRunVariable<bool>>().Single(v => v.Name == "boolVariableKey");
        Assert.False(boolVariable.Value);

        Assert.Empty(state.PipelineActivityResults);
        Assert.Empty(state.ScopedPipelineActivityResults);
        Assert.Null(state.IterationItem);
    }

    [Fact]
    public void WhenActivityResultAreAdded_ShouldBeAddedCorrectly()
    {
        // Arrange
        var state = new PipelineRunState();
        var activityResult = new TestActivityResult("activityName", DependencyCondition.Succeeded);

        // Act
        state.AddActivityResult(activityResult);

        // Assert
        Assert.Single(state.PipelineActivityResults);
        Assert.Equal(activityResult, state.PipelineActivityResults.Single());
        Assert.Single(state.ScopedPipelineActivityResults);
        Assert.Equal(activityResult, state.ScopedPipelineActivityResults.Single());
    }

    [Fact]
    public void WhenAddScopedActivityResultsFromScopedState_ShouldRegisterScopedResults()
    {
        // Arrange
        var scopedState = new PipelineRunState();
        scopedState.AddActivityResult(new TestActivityResult("activityName", DependencyCondition.Succeeded));
        var state = new PipelineRunState();

        // Act
        state.AddScopedActivityResultsFromScopedState(scopedState);

        // Assert
        Assert.Single(state.PipelineActivityResults);
        Assert.Equal(scopedState.ScopedPipelineActivityResults.Single(), state.PipelineActivityResults.Single());
    }

    [Fact]
    public void WhenIterationScopedIsCreated_ShouldReturnNewScopeWithIterationItem()
    {
        // Arrange
        var state = new PipelineRunState();
        state.AddActivityResult(new TestActivityResult("activityName", DependencyCondition.Succeeded));
        state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "parameterKey", "parameterValue"));
        state.Variables.Add(new PipelineRunVariable<string>("variableKey", "variableValue"));

        // Act
        var scopedState = state.CreateIterationScope("iterationItem");

        // Assert
        Assert.Equal("iterationItem", scopedState.IterationItem);
        Assert.Equal(state.Parameters, scopedState.Parameters);
        Assert.Equal(state.Variables, scopedState.Variables);
        Assert.Equal(state.PipelineActivityResults, scopedState.PipelineActivityResults);
        Assert.Empty(scopedState.ScopedPipelineActivityResults);
    }
}