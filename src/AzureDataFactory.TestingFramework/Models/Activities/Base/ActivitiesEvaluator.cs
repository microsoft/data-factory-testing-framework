using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models.Activities.Base;

public static class ActivitiesEvaluator
{
    public static IEnumerable<PipelineActivity> Evaluate(List<PipelineActivity> activities, PipelineRunState state)
    {
        while (state.PipelineActivityResults.Count != activities.Count)
        {
            var anyActivityEvaluated = false;
            foreach (var activity in activities
                         .Where(activity => !state.PipelineActivityResults.Contains(activity))
                         .Where(activity => activity.AreDependencyConditionMet(state)))
            {
                yield return (PipelineActivity) activity.Evaluate(state);
                anyActivityEvaluated = true;
                state.AddActivityResult(activity);

                if (activity is ControlActivity controlActivity)
                {
                    if (controlActivity is UntilActivity untilActivity)
                    {
                        while (untilActivity.Expression.Evaluate<bool>(state))
                            foreach (var child in untilActivity.EvaluateChildActivities(state))
                                yield return child;
                    }
                    else
                    {
                        foreach (var child in controlActivity.EvaluateChildActivities(state))
                            yield return child;
                    }
                }
            }

            if (!anyActivityEvaluated)
            {
                throw new Exception("Dependencies could not be evaluated");
            }
        }
    }
}