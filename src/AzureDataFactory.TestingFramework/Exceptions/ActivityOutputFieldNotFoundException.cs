// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ActivityOutputFieldNotFoundException : Exception
{
    public ActivityOutputFieldNotFoundException(string activityName, string field) : base($"The field {field} was not found on the activity: {activityName}. Set the activity results to include the field.")
    {
    }
}