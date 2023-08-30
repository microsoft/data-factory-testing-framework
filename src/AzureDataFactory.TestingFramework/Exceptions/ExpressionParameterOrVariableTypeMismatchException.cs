using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Expressions;

public class ExpressionParameterOrVariableTypeMismatchException : Exception
{
    public ExpressionParameterOrVariableTypeMismatchException(string parameterName, Type type) : base($"Parameter {parameterName} is not of expectedtype {type.Name}")
    {
    }
    public ExpressionParameterOrVariableTypeMismatchException(string parameterName, ParameterType parameterType, Type type) : base($"{parameterType} parameter {parameterName} is not of expectedtype {type.Name}")
    {
    }
}