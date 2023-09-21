// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Models.Base;

public interface IRunParameter
{
    public string Name { get; }
    public ParameterType Type { get; }
}
public class RunParameter<TValueType> : IRunParameter
{
    /// <summary>
    /// Initializes a new instance of the <see cref="RunParameter{TValueType}"/> class. Can be passed to a pipeline evaluation run.
    /// </summary>
    /// <param name="type">The type of the parameter (e.g. parameter, global, dataset, LinkedService).</param>
    /// <param name="name">The name of the parameter. Must match the name of the parameter in the pipeline being targeted.</param>
    /// <param name="value">The value of the parameter</param>
    public RunParameter(ParameterType type, string name, TValueType value)
    {
        Name = name;
        Type = type;
        Value = value;
    }

    /// <summary>
    /// The name of the parameter. Must match the name of the parameter in the pipeline being targeted.
    /// </summary>
    public string Name { get; }

    /// <summary>
    /// The type of the parameter (e.g. parameter, global, dataset, LinkedService).
    /// </summary>
    public ParameterType Type { get; }

    /// <summary>
    /// The value of the parameter
    /// </summary>
    public TValueType Value { get; }
}