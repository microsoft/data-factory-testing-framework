// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

internal class LinkedServiceParameterNotFoundException : Exception
{
    public LinkedServiceParameterNotFoundException(string parameterExpressionParameterName) : base(
        $"Parameter with name {parameterExpressionParameterName} was not found.")
    {
    }
}