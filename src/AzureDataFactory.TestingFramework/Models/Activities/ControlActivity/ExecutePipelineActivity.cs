// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class ExecutePipelineActivity : IIterationActivity
{
    internal List<IRunParameter> GetChildRunParameters(PipelineRunState state)
    {
        var parameters = state.Parameters.Where(p => p.Type == ParameterType.Global).ToList();
        parameters.AddRange(Parameters.Select(p => new RunParameter<string>(ParameterType.Pipeline, p.Key, p.Value)));
        return parameters;
    }
}
