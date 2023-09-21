// Copyright (c) Microsoft Corporation.

using Azure;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Models.Pipelines;

/// <summary>
/// The pipeline run state stores the state of the pipeline run just like Azure Data Factory would do. It stores the parameters and variables and the results of the activities.
/// </summary>
public class PipelineRunState : RunState
{
    /// <summary>
    /// The variables of a pipeline run. Can be set upon creation of the state or during the evaluation of the SetVariable activities.
    /// </summary>
    public List<IPipelineRunVariable> Variables { get; }

    /// <summary>
    /// The current item() of a ForEach activity.
    /// </summary>
    public string? IterationItem { get; set; }

    /// <summary>
    /// The complete list of activity results of the pipeline run so far.
    /// </summary>
    public List<IPipelineActivityResult> PipelineActivityResults { get; }

    /// <summary>
    /// The scoped list of activity results of the pipeline run so far. A scope is created for each ControlActivity like ForEach, If and Until activities.
    /// </summary>
    public List<IPipelineActivityResult> ScopedPipelineActivityResults { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="PipelineRunState"/> class.
    /// </summary>
    /// <param name="parameters">The global and regular parameters to be used for evaluating expressions.</param>
    /// <param name="variables">The initial variables specification to use for the pipeline run.</param>
    public PipelineRunState(List<IRunParameter> parameters, IDictionary<string, PipelineVariableSpecification> variables) : base(parameters)
    {
        Variables = variables.Select(variable =>
        {
            if (variable.Value.VariableType == PipelineVariableType.String)
                return new PipelineRunVariable<string>(variable.Key, variable.Value.DefaultValue?.ToString());

            if (variable.Value.VariableType == PipelineVariableType.Bool)
                return new PipelineRunVariable<bool>(variable.Key, variable.Value.DefaultValue != null && bool.Parse(variable.Value.DefaultValue.ToString()));

            // TODO: better arrays support
            if (variable.Value.VariableType == PipelineVariableType.Array)
                return (IPipelineRunVariable)new PipelineRunVariable<string>(variable.Key, variable.Value.DefaultValue?.ToString());

            throw new NotImplementedException($"Unknown variable type: {variable.Value.VariableType}");
        }).ToList();
        PipelineActivityResults = new List<IPipelineActivityResult>();
        ScopedPipelineActivityResults = new List<IPipelineActivityResult>();
        IterationItem = null;
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="PipelineRunState"/> class.
    /// </summary>
    /// <param name="parameters">The global and regular parameters to be used for evaluating expressions.</param>
    /// <param name="variables">The initial variables specification to use for the pipeline run.</param>
    /// <param name="activityResults">The results of previous activities to use for validating dependencyConditions and evaluating expressions (i.e. activity('activityName').output)</param>
    /// <param name="iterationItem">The current item() of a ForEach activity.</param>
    public PipelineRunState(List<IRunParameter> parameters, List<IPipelineRunVariable> variables, List<IPipelineActivityResult> activityResults, string? iterationItem) : base(parameters)
    {
        Variables = variables;
        PipelineActivityResults = new List<IPipelineActivityResult>();
        PipelineActivityResults.AddRange(activityResults);
        ScopedPipelineActivityResults = new List<IPipelineActivityResult>();
        IterationItem = iterationItem;
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="PipelineRunState"/> class.
    /// </summary>
    public PipelineRunState() : base(new List<IRunParameter>())
    {
        Variables = new List<IPipelineRunVariable>();
        PipelineActivityResults = new List<IPipelineActivityResult>();
        ScopedPipelineActivityResults = new List<IPipelineActivityResult>();
        IterationItem = null;
    }

    /// <summary>
    /// Registers the result of an activity to the pipeline run state.
    /// </summary>
    /// <param name="pipelineActivityResult">The results of previous activities to use for validating dependencyConditions and evaluating expressions (i.e. activity('activityName').output)</param>
    public void AddActivityResult(IPipelineActivityResult pipelineActivityResult)
    {
        ScopedPipelineActivityResults.Add(pipelineActivityResult);
        PipelineActivityResults.Add(pipelineActivityResult);
    }

    /// <summary>
    /// Registers all the activity results of a childScope into the current state.
    /// </summary>
    /// <param name="scopedState">The scoped childState</param>
    public void AddScopedActivityResultsFromScopedState(PipelineRunState scopedState)
    {
        PipelineActivityResults.AddRange(scopedState.ScopedPipelineActivityResults);
    }

    /// <summary>
    /// Used to create a new scope for a ControlActivity like ForEach, If and Until activities.
    /// </summary>
    /// <param name="iterationItem">Should only be set for ForEach activities</param>
    /// <returns></returns>
    public PipelineRunState CreateIterationScope(string? iterationItem)
    {
        return new PipelineRunState(Parameters, Variables, PipelineActivityResults, iterationItem);
    }
}