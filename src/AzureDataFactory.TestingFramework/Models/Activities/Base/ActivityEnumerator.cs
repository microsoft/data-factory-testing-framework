// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Exceptions;

namespace AzureDataFactory.TestingFramework.Models.Activities.Base;

public class ActivityEnumerator
{
    private readonly IEnumerator<PipelineActivity> _enumerator;

    /// <summary>
    /// Initializes a new instance of the <see cref="ActivityEnumerator"/> class. Can be used to easily iterate over a list of activities one by one.
    /// </summary>
    /// <param name="activities"></param>
    public ActivityEnumerator(IEnumerable<PipelineActivity> activities)
    {
        _enumerator = activities.GetEnumerator();
    }

    /// <summary>
    /// Moves the enumerator to the next activity and returns it.
    /// </summary>
    /// <returns>The next activity</returns>
    /// <exception cref="ActivityEnumeratorException">If there are no more activities available for evaluation</exception>
    public PipelineActivity GetNext()
    {
        if (_enumerator.MoveNext())
            return _enumerator.Current!;

        throw new ActivityEnumeratorException("No more activities to evaluate");
    }

    /// <summary>
    /// Moves the enumerator to the next activity and returns it.
    /// </summary>
    /// <returns>The next activity</returns>
    /// <exception cref="ActivityEnumeratorException">If there are no more activities available for evaluation</exception>
    /// <exception cref="ActivityEnumeratorTypeMismatchException">If the returned activity is of a different type than requested</exception>
    public TActivityType GetNext<TActivityType>() where TActivityType : PipelineActivity
    {
        if (_enumerator.MoveNext())
            return _enumerator.Current as TActivityType ?? throw new ActivityEnumeratorTypeMismatchException($"Expected activity of type {typeof(TActivityType).Name} but found activity of type {_enumerator.Current?.GetType().Name}");

        throw new ActivityEnumeratorException("No more activities to evaluate");
    }
}