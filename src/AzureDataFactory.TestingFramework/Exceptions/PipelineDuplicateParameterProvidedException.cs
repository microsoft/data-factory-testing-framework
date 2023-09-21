// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class PipelineDuplicateParameterProvidedException : Exception
{
    public PipelineDuplicateParameterProvidedException(string message) : base(message)
    {
    }
}