// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class PipelineParameterNotProvidedException : Exception
{
    public PipelineParameterNotProvidedException(string message) : base(message)
    {
    }
}