using AzureDataFactory.TestingFramework.Exceptions;

namespace AzureDataFactory.TestingFramework.Models.Activities.Base;

public class ActivityEnumerator
{
    private readonly IEnumerator<PipelineActivity> _enumerator;

    public ActivityEnumerator(IEnumerable<PipelineActivity> activities)
    {
        _enumerator = activities.GetEnumerator();
    }

    public PipelineActivity GetNext()
    {
        if (_enumerator.MoveNext())
            return _enumerator.Current!;

        throw new ActivityEnumeratorException("No more activities to evaluate");
    }
}