// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace Azure.ResourceManager.DataFactory;

public partial class Pipeline
{
    public PipelineActivity GetActivityByName(string activityName)
    {
        return Activities.SingleOrDefault(activity => activity.Name == activityName) ?? throw new ActivityNotFoundException(activityName);
    }

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

    public ActivityEnumerator EvaluateWithActivityEnumerator(List<IRunParameter> parameters)
    {
        var activities = Evaluate(parameters);
        return new ActivityEnumerator(activities);
    }
}