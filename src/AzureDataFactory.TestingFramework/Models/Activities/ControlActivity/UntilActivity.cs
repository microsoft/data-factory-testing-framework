using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class UntilActivity
{
    protected override List<PipelineActivity> GetNextActivities()
    {
        return Activities.ToList();
    }

    private bool? _evaluatedExpression;
    public override PipelineActivity Evaluate(PipelineRunState state)
    {
        base.Evaluate(state);

        _evaluatedExpression = Expression.Evaluate<bool>(state);

        return this;
    }
}