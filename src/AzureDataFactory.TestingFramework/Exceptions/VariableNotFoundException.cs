// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

internal class VariableNotFoundException : Exception
{
    public VariableNotFoundException(string variableExpressionVariableName) : base(
        $"Variable with name {variableExpressionVariableName} was not found.")
    {
    }
}