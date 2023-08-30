using Azure;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Models.Pipelines;

public class PipelineRunState : RunState
{
    public List<IPipelineRunVariable> Variables { get; }
    public string? IterationItem { get; set; }
    public List<IPipelineActivityResult> PipelineActivityResults { get; }

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
                return (IPipelineRunVariable) new PipelineRunVariable<string>(variable.Key, variable.Value.DefaultValue?.ToString());

            throw new Exception($"Unknown variable type: {variable.Value.VariableType}");
        }).ToList();;
        PipelineActivityResults = new List<IPipelineActivityResult>();
        IterationItem = null;
    }

    public PipelineRunState(List<IRunParameter> parameters, List<IPipelineRunVariable> variables, string? iterationItem) : base(parameters)
    {
        Variables = variables;
        PipelineActivityResults = new List<IPipelineActivityResult>();
        IterationItem = iterationItem;
    }

    public PipelineRunState(): base(new List<IRunParameter>())
    {
        Variables = new List<IPipelineRunVariable>();
        PipelineActivityResults = new List<IPipelineActivityResult>();
        IterationItem = null;
    }

    public void AddActivityResult(IPipelineActivityResult pipelineActivityResult)
    {
        PipelineActivityResults.Add(pipelineActivityResult);
    }

    public PipelineRunState CreateIterationScope(string? iterationItem)
    {
        return new PipelineRunState(Parameters, Variables, iterationItem);
    }
}