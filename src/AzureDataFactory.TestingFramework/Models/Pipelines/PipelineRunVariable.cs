// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Models.Pipelines;

public interface IPipelineRunVariable
{
    public string Name { get; }
}
public class PipelineRunVariable<TType> : IPipelineRunVariable
{
    public PipelineRunVariable(string name, TType? defaultValue = default)
    {
        Name = name;
        Value = defaultValue;
    }

    public string Name { get; }
    public TType? Value { get; set; }
}