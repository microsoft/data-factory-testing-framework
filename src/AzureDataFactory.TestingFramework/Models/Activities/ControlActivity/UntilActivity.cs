// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class UntilActivity : IIterationActivity
{
    internal override IEnumerable<PipelineActivity> EvaluateControlActivityIterations(PipelineRunState state, EvaluateActivitiesDelegate evaluateActivities)
    {
        do
        {
            var scopedState = state.CreateIterationScope(null);
            foreach (var child in evaluateActivities(Activities.ToList(), scopedState))
                yield return child;

            state.AddScopedActivityResultsFromScopedState(scopedState);
        } while (!Expression.Evaluate<bool>(state));
    }
}