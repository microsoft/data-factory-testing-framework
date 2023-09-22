// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ActivityEnumeratorException : Exception
{
    public ActivityEnumeratorException(string message) : base(message)
    {
    }
}