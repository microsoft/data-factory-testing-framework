// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace Azure.ResourceManager.DataFactory;

public partial class Pipeline
{
    /// <summary>
    /// Gets the activity by name.
    /// </summary>
    /// <param name="activityName">Name of the activity as described in `name` field of the activity</param>
    /// <returns></returns>
    /// <exception cref="ActivityNotFoundException">Thrown if activity name cannot be found</exception>
    public PipelineActivity GetActivityByName(string activityName)
    {
        return Activities.SingleOrDefault(activity => activity.Name == activityName) ?? throw new ActivityNotFoundException(activityName);
    }

    /// <summary>
    /// Validates whether the list of parameters are complete and not duplicate.
    /// </summary>
    /// <param name="parameters"></param>
    /// <exception cref="PipelineParameterNotProvidedException">Thrown if a required pipeline parameter is not required</exception>
    /// <exception cref="PipelineDuplicateParameterProvidedException">Thrown if a pipeline parameter is provided more than once</exception>
    internal void ValidateParameters(List<IRunParameter> parameters)
    {
        //Check if all parameters are provided
        foreach (var parameter in Parameters.Where(parameter => parameters.All(p => p.Name != parameter.Key)))
            throw new PipelineParameterNotProvidedException($"Parameter {parameter.Key} is not provided");

        // Check if no duplicate parameters are provided
        var duplicateParameters = parameters.GroupBy(x => new { x.Name, x.Type }).Where(g => g.Count() > 1).Select(y => y.Key).ToList();
        if (duplicateParameters.Any())
            throw new PipelineDuplicateParameterProvidedException($"Duplicate parameters provided: {string.Join(", ", duplicateParameters.Select(x => $"{x.Name} ({x.Type})"))}");
    }
}