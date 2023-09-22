// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Models.Base;

public class RunState
{
    /// <summary>
    /// Initializes a new instance of the <see cref="RunState"/> class. Can be used to purely evaluate an activity in a non-pipeline context.
    /// </summary>
    /// <param name="parameters">The name of the parameter. Must match the name of the parameter in the pipeline being targeted.</param>
    public RunState(List<IRunParameter> parameters)
    {
        Parameters = parameters;
    }

    /// <summary>
    /// The name of the parameter. Must match the name of the parameter in the pipeline being targeted.
    /// </summary>
    public List<IRunParameter> Parameters { get; }
}