// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ExpressionEvaluatedToNullException : Exception
{
    public ExpressionEvaluatedToNullException(string message) : base(message)
    { }

}