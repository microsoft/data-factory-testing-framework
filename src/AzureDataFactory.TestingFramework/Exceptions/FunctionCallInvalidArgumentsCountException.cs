using System.Reflection;
using AzureDataFactory.TestingFramework.Functions;

namespace AzureDataFactory.TestingFramework.Exceptions;

public class FunctionCallInvalidArgumentsCountException : Exception
{
    public FunctionCallInvalidArgumentsCountException(string name, List<object> evaluatedArguments, ParameterInfo[] parameters) : base($"FunctionCall {name} has invalid arguments count. Evaluated arguments: \"{string.Join("\", \"", evaluatedArguments)}\". Expected argument types: {string.Join(", ", parameters.Select(p => p.ParameterType))}")
    {
    }
    public FunctionCallInvalidArgumentsCountException(string name, List<IFunctionPart> arguments, ParameterInfo[] parameters) : base($"FunctionCall {name} has invalid arguments count. Evaluated arguments: \"{string.Join("\", \"", arguments)}\". Expected argument types: {string.Join(", ", parameters.Select(p => p.ParameterType))}")
    {
    }
}