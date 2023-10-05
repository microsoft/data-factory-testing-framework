// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Azure.ResourceManager.DataFactory;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;
using AzureDataFactory.TestingFramework.Models.Repositories;

namespace AzureDataFactory.TestingFramework.Models;

public class TestFramework
{
    private readonly bool _shouldEvaluateChildPipelines;
    public DataFactoryRepository Repository { get; }

    public TestFramework(string? dataFactoryFolderPath = null, bool shouldEvaluateChildPipelines = false)
    {
        Repository = dataFactoryFolderPath != null ? DataFactoryRepositoryFactory.ParseFromFolder(dataFactoryFolderPath) : new DataFactoryRepository();
        _shouldEvaluateChildPipelines = shouldEvaluateChildPipelines;
    }

    /// <summary>
    /// Get an enumerator to yield the evaluation of the pipeline activities one by one using the provided parameters. The order of activity execution is simulated based on the dependencies. Any expression part of the activity is evaluated based on the state of the pipeline.
    /// </summary>
    /// <param name="pipeline">The pipeline to evaluate.</param>
    /// <param name="parameters">The global and regular parameters to be used for evaluating expressions.</param>
    /// <returns></returns>
    /// <exception cref="PipelineParameterNotProvidedException">Thrown if a required pipeline parameter is not required</exception>
    /// <exception cref="PipelineDuplicateParameterProvidedException">Thrown if a pipeline parameter is provided more than once</exception>
    public IEnumerable<PipelineActivity> Evaluate(Pipeline pipeline, List<IRunParameter> parameters)
    {
        pipeline.ValidateParameters(parameters);
        var state = new PipelineRunState(parameters, pipeline.Variables);
        return Evaluate(pipeline.Activities.ToList(), state);
    }

    public ActivityEnumerator EvaluateWithEnumerator(Pipeline pipeline, List<IRunParameter> parameters)
    {
        return new ActivityEnumerator(Evaluate(pipeline, parameters));
    }

    /// <summary>
    /// Evaluates all pipeline activities using the provided parameters. The order of activity execution is simulated based on the dependencies. Any expression part of the activity is evaluated based on the state of the pipeline.
    /// </summary>
    /// <param name="pipeline">The pipeline to evaluate.</param>
    /// <param name="parameters">The global and regular parameters to be used for evaluating expressions.</param>
    /// <returns></returns>
    /// <exception cref="PipelineParameterNotProvidedException">Thrown if a required pipeline parameter is not required</exception>
    /// <exception cref="PipelineDuplicateParameterProvidedException">Thrown if a pipeline parameter is provided more than once</exception>
    public List<PipelineActivity> EvaluateAll(Pipeline pipeline, List<IRunParameter> parameters)
    {
        return Evaluate(pipeline, parameters).ToList();
    }

    public IEnumerable<PipelineActivity> Evaluate(PipelineActivity activity, PipelineRunState state)
    {
        return Evaluate(new List<PipelineActivity> { activity }, state);
    }

    public IEnumerable<PipelineActivity> Evaluate(List<PipelineActivity> activities, PipelineRunState state)
    {
        while (state.ScopedPipelineActivityResults.Count != activities.Count)
        {
            var anyActivityEvaluated = false;
            foreach (var activity in activities
                         .Where(activity => !state.ScopedPipelineActivityResults.Contains(activity))
                         .Where(activity => activity.AreDependencyConditionMet(state)))
            {
                var evaluatedActivity = (PipelineActivity)activity.Evaluate(state);
                if (evaluatedActivity is not IIterationActivity || (evaluatedActivity is ExecutePipelineActivity && !_shouldEvaluateChildPipelines))
                    yield return evaluatedActivity;

                anyActivityEvaluated = true;
                state.AddActivityResult(activity);

                if (activity is IIterationActivity)
                {
                    if (activity is ExecutePipelineActivity executePipelineActivity && _shouldEvaluateChildPipelines)
                    {
                        var pipeline = Repository.GetPipelineByName(executePipelineActivity.Pipeline.ReferenceName);

                        // Evaluate the pipeline with its own scope
                        foreach (var childActivity in Evaluate(pipeline, executePipelineActivity.GetChildRunParameters(state)))
                            yield return childActivity;
                    }
                    else if (activity is ControlActivity controlActivity)
                    {
                        foreach (var childActivity in controlActivity.EvaluateControlActivityIterations(state, Evaluate))
                            yield return childActivity;
                    }
                }
            }

            if (!anyActivityEvaluated)
            {
                throw new ActivitiesEvaluatorInvalidDependencyException("Validate that there are no circular dependencies or whether activity results were not set correctly.");
            }
        }
    }
}
