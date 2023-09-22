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
    /// Evaluates the pipeline with the provided parameters. The order of activity execution is simulated based on the dependencies. Any expression part of the activity is evaluated based on the state of the pipeline.
    /// </summary>
    /// <param name="parameters">The global and regular parameters to be used for evaluating expressions.</param>
    /// <returns></returns>
    /// <exception cref="PipelineParameterNotProvidedException">Thrown if a required pipeline parameter is not required</exception>
    /// <exception cref="PipelineDuplicateParameterProvidedException">Thrown if a pipeline parameter is provided more than once</exception>
    public IEnumerable<PipelineActivity> Evaluate(List<IRunParameter> parameters)
    {
        //Check if all parameters are provided
        foreach (var parameter in Parameters.Where(parameter => parameters.All(p => p.Name != parameter.Key)))
            throw new PipelineParameterNotProvidedException($"Parameter {parameter.Key} is not provided");

        // Check if no duplicate parameters are provided
        var duplicateParameters = parameters.GroupBy(x => new { x.Name, x.Type }).Where(g => g.Count() > 1).Select(y => y.Key).ToList();
        if (duplicateParameters.Any())
            throw new PipelineDuplicateParameterProvidedException($"Duplicate parameters provided: {string.Join(", ", duplicateParameters.Select(x => $"{x.Name} ({x.Type})"))}");

        var state = new PipelineRunState(parameters, Variables);
        foreach (var activity in ActivitiesEvaluator.Evaluate(Activities.ToList(), state))
            yield return activity;
    }

    /// <summary>
    /// Evaluates the pipeline with the provider parameters and returns an enumerator to easily iterate over the activities. The order of activity execution is simulated based on the dependencies. Any expression part of the activity is evaluated based on the state of the pipeline.
    /// </summary>
    /// <param name="parameters">The global and regular parameters to be used for evaluating expressions.</param>
    /// <returns></returns>
    /// <exception cref="PipelineParameterNotProvidedException">Thrown if a required pipeline parameter is not required</exception>
    /// <exception cref="PipelineDuplicateParameterProvidedException">Thrown if a pipeline parameter is provided more than once</exception>
    public ActivityEnumerator EvaluateWithActivityEnumerator(List<IRunParameter> parameters)
    {
        var activities = Evaluate(parameters);
        return new ActivityEnumerator(activities);
    }
}