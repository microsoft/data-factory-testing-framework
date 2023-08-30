namespace AzureDataFactory.TestingFramework.Exceptions;

public class VariableBeingEvaluatedDoesNotExistException : Exception
{
    public VariableBeingEvaluatedDoesNotExistException(string variableName) : base($"Variable with name {variableName} does not exist in the pipeline")
    {
    }
}