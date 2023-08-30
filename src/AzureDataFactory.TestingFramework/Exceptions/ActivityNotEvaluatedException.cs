namespace AzureDataFactory.TestingFramework.Exceptions;

public class ActivityNotEvaluatedException : Exception
{
    public ActivityNotEvaluatedException(string activityName) : base($"Activity {activityName} was not evaluated.")
    {
    }
}