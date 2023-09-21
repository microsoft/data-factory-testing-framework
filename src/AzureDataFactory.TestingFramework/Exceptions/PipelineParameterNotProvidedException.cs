// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class PipelineParameterNotProvidedException : Exception
{
    public PipelineParameterNotProvidedException(string message) : base(message)
    {
    }
}