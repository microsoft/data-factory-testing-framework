using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class IfConditionActivity
{
    protected override List<PipelineActivity> GetNextActivities()
    {
        return _evaluatedExpression.Value ? IfTrueActivities.ToList() : IfFalseActivities.ToList();
    }

    public bool? _evaluatedExpression;
    public bool EvaluatedExpression => _evaluatedExpression ?? throw new InvalidOperationException("Expression has not been evaluated yet.");
    public override DataFactoryEntity Evaluate(PipelineRunState state)
    {
        base.Evaluate(state);

        _evaluatedExpression = Expression.Evaluate<bool>(state);

        return this;
    }
}