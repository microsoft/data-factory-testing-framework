// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Models.Activities.Base;

public interface IPipelineActivityResult
{
    public string Name { get; }
    public DependencyCondition? Status { get; }
    public object Output { get; }
}