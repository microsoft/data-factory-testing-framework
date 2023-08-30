using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Exceptions;

public class ExpressionParameterNotFoundException : Exception
{
    public ExpressionParameterNotFoundException(string parameterName) : base($"parameter with name: '{parameterName}' not found")
    {
    }
    public ExpressionParameterNotFoundException(string parameterName, ParameterType type) : base($"{type} parameter with name: '{parameterName}' not found")
    {
    }
}