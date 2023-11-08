// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class IfConditionActivity : IIterationActivity
{
    private bool? _evaluatedExpression;
    public bool EvaluatedExpression => _evaluatedExpression ?? throw new InvalidOperationException("Expression has not been evaluated yet.");
    public override DataFactoryEntity Evaluate(PipelineRunState state)
    {
        base.Evaluate(state);

        _evaluatedExpression = Expression.Evaluate<bool>(state);

        return this;
    }

    internal override IEnumerable<PipelineActivity> EvaluateControlActivityIterations(PipelineRunState state, EvaluateActivitiesDelegate evaluateActivities)
    {
        var scopedState = state.CreateIterationScope(null);
        var activities = EvaluatedExpression ? IfTrueActivities.ToList() : IfFalseActivities.ToList();
        foreach (var activity in evaluateActivities(activities, scopedState))
            yield return activity;

        state.AddScopedActivityResultsFromScopedState(scopedState);
    }
}