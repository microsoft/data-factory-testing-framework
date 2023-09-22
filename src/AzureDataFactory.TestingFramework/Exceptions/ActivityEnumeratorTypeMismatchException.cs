// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ActivityEnumeratorTypeMismatchException : Exception
{
    public ActivityEnumeratorTypeMismatchException(string message) : base(message)
    {
    }
}