// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

internal class ParameterNotFoundException : Exception
{
    public ParameterNotFoundException(string parameterExpressionParameterName) : base(
        $"Parameter with name {parameterExpressionParameterName} was not found.")
    {
    }
}