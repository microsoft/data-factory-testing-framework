// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Models.Pipelines;

public interface IPipelineRunVariable
{
    public string Name { get; }
}
public class PipelineRunVariable<TType> : IPipelineRunVariable
{
    /// <summary>
    /// Initializes a new instance of the <see cref="PipelineRunVariable{TType}"/> class. To be used for defining initial state of variables for a pipeline run.
    /// </summary>
    /// <param name="name">Name of the variable</param>
    /// <param name="defaultValue">Initial value to set for this variable</param>
    public PipelineRunVariable(string name, TType? defaultValue = default)
    {
        Name = name;
        Value = defaultValue;
    }

    /// <summary>
    /// The name of the variable as defined in the pipeline.
    /// </summary>
    public string Name { get; }

    /// <summary>
    /// The value of the variable. Can be set during the evaluation of the SetVariable activity.
    /// </summary>
    public TType? Value { get; set; }
}