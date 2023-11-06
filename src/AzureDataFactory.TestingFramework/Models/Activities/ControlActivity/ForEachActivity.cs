// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class ForEachActivity : IIterationActivity
{
    private List<string>? _items;
    public List<string> IterationItems => _items ?? throw new InvalidOperationException("Items have not been evaluated yet.");
    public override DataFactoryEntity Evaluate(PipelineRunState state)
    {
        _items = Items.Evaluate<List<string>>(state);

        return base.Evaluate(state);
    }

    internal override IEnumerable<PipelineActivity> EvaluateControlActivityIterations(PipelineRunState state, EvaluateActivitiesDelegate evaluateActivities)
    {
        // Note: using enumerator to support yield return in foreach
        using var enumerator = IterationItems.GetEnumerator();
        while (enumerator.MoveNext())
        {
            var scopedState = state.CreateIterationScope(enumerator.Current);
            foreach (var activity in evaluateActivities(Activities.ToList(), scopedState))
                yield return activity;

            state.AddScopedActivityResultsFromScopedState(scopedState);
        }
    }
}