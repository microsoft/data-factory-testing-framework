// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class PipelineDuplicateParameterProvidedException : Exception
{
    public PipelineDuplicateParameterProvidedException(string message) : base(message)
    {
    }
}