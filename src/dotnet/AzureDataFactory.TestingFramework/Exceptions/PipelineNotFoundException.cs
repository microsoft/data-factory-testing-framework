// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class PipelineNotFoundException : Exception
{
    public PipelineNotFoundException(string name) : base($"Pipeline with name '{name}' was not found in the repository. Make sure to load the repository before evaluating pipelines.")
    {
    }
}
