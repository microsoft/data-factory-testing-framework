// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

internal class VariableNotFoundException : Exception
{
    public VariableNotFoundException(string variableExpressionVariableName) : base(
        $"Variable with name {variableExpressionVariableName} was not found.")
    {
    }
}