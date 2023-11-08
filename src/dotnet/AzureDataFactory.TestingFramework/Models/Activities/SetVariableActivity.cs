// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class SetVariableActivity
{
    public override PipelineActivity Evaluate(PipelineRunState state)
    {
        base.Evaluate(state);

        // If SetVariable is used for setting return values, local variables are ignored
        if (VariableName == "pipelineReturnValue")
            return this;

        var existingVariable = state.Variables.SingleOrDefault(variable => variable.Name == VariableName) ??
                               throw new VariableBeingEvaluatedDoesNotExistException(VariableName);

        var result = Value.Evaluate(state);
        if (existingVariable is PipelineRunVariable<string> existingStringVariable)
            existingStringVariable.Value = result;
        else if (existingVariable is PipelineRunVariable<bool> existingBoolVariable)
            existingBoolVariable.Value = bool.Parse(result);
        else
            throw new Exception($"Unknown variable type: {existingVariable.GetType().Name}");

        return this;
    }
}