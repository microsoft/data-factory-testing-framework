// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ExpressionEvaluatedToWrongTypeException : Exception
{
    public ExpressionEvaluatedToWrongTypeException(Type type, Type getType) : base($"Expression evaluated to wrong type. Expected: {type.Name}, Actual: {getType.Name}")
    {
    }
}