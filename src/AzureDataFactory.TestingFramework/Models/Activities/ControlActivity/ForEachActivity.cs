// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class ForEachActivity : IIterationActivity
{
    protected override List<PipelineActivity> GetNextActivities()
    {
        return Activities.ToList();
    }

    private List<string>? _items;
    public List<string> IterationItems => _items ?? throw new InvalidOperationException("Items have not been evaluated yet.");
    public override DataFactoryEntity Evaluate(PipelineRunState state)
    {
        _items = Items.Evaluate<List<string>>(state);

        return base.Evaluate(state);
    }

    public override IEnumerable<PipelineActivity> EvaluateChildActivities(PipelineRunState state)
    {
        var activities = GetNextActivities();

        return IterationItems.SelectMany(item =>
        {
            var scopedState = state.CreateIterationScope(item);
            return ActivitiesEvaluator.Evaluate(activities, scopedState);
        });
    }
}