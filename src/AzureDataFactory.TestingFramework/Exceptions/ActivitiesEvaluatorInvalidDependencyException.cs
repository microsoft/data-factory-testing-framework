// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ActivitiesEvaluatorInvalidDependencyException : Exception
{
    public ActivitiesEvaluatorInvalidDependencyException(string message) : base(message)
    {

    }
}