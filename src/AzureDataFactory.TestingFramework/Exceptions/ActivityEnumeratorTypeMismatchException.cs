// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ActivityEnumeratorTypeMismatchException : Exception
{
    public ActivityEnumeratorTypeMismatchException(string message) : base(message)
    {
    }
}