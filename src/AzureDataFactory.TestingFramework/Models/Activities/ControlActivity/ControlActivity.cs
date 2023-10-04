// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class ControlActivity
{
    protected virtual List<PipelineActivity> GetNextActivities()
    {
        return new List<PipelineActivity>();
    }

    internal virtual IEnumerable<PipelineActivity> EvaluateChildActivities(PipelineRunState state, TestFramework testFramework)
    {
        var scopedState = state.CreateIterationScope(null);
        var activities = GetNextActivities();
        foreach (var activity in testFramework.EvaluateActivities(activities, scopedState))
        {
            yield return activity;
        }

        state.AddScopedActivityResultsFromScopedState(scopedState);
    }

    internal virtual IEnumerable<PipelineActivity> EvaluateChildActivities(PipelineRunState state)
    {
        return EvaluateChildActivities(state, new TestFramework());
    }
}