// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class IfConditionActivity : IIterationActivity
{
    protected override List<PipelineActivity> GetNextActivities()
    {
        return EvaluatedExpression ? IfTrueActivities.ToList() : IfFalseActivities.ToList();
    }

    private bool? _evaluatedExpression;
    public bool EvaluatedExpression => _evaluatedExpression ?? throw new InvalidOperationException("Expression has not been evaluated yet.");
    public override DataFactoryEntity Evaluate(PipelineRunState state)
    {
        base.Evaluate(state);

        _evaluatedExpression = Expression.Evaluate<bool>(state);

        return this;
    }
}