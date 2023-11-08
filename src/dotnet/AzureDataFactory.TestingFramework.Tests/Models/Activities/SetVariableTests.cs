// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models.Activities;

public class SetVariableTests
{
    [Fact]
    public void WhenStringVariableEvaluated_ThenStateVariableShouldBeSet()
    {
        // Arrange
        var variableName = "TestVariable";
        var variable = new PipelineRunVariable<string>(variableName, string.Empty);
        var setVariable = new SetVariableActivity("TestSetVariable")
        {
            VariableName = variableName,
            Value = "value1"
        };
        var state = new PipelineRunState();
        state.Variables.Add(variable);

        // Act
        setVariable.Evaluate(state);

        // Assert
        Assert.Equal("value1", variable.Value);
    }
}