// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Expressions;

public class TypeOfPipelineActivityResultDoesNotMatchExpectedType : Exception
{
    public TypeOfPipelineActivityResultDoesNotMatchExpectedType(string activityName, string field, Type actualType, Type expectedType) : base($"The type of the activity output field '{field}' on activity '{activityName}' is '{actualType.Name}' but the expected type is '{expectedType.Name}'")
    {
    }
}