using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models.Activities.Base;

public static class ActivitiesEvaluator
{
    public static IEnumerable<PipelineActivity> Evaluate(List<PipelineActivity> activities, PipelineRunState state)
    {
        while (state.ScopedPipelineActivityResults.Count != activities.Count)
        {
            var anyActivityEvaluated = false;
            foreach (var activity in activities
                         .Where(activity => !state.ScopedPipelineActivityResults.Contains(activity))
                         .Where(activity => activity.AreDependencyConditionMet(state)))
            {
                var evaluatedActivity = (PipelineActivity) activity.Evaluate(state);
                if (evaluatedActivity is not IIterationActivity)
                    yield return evaluatedActivity;

                anyActivityEvaluated = true;
                state.AddActivityResult(activity);

                if (activity is IIterationActivity)
                {
                    if (activity is UntilActivity untilActivity)
                    {
                        do
                        {
                            foreach (var child in untilActivity.EvaluateChildActivities(state))
                                yield return child;
                        } while (!untilActivity.Expression.Evaluate<bool>(state));
                    }
                    else if (activity is ControlActivity controlActivity)
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