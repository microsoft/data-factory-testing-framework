// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

internal class LinkedServiceParameterNotFoundException : Exception
{
    public LinkedServiceParameterNotFoundException(string parameterExpressionParameterName) : base(
        $"Parameter with name {parameterExpressionParameterName} was not found.")
    {
    }
}