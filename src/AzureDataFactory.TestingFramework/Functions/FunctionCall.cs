// Copyright (c) Microsoft Corporation.

using System.Reflection;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Functions;

public class FunctionCall : IFunctionPart
{
    public FunctionCall(string name, List<IFunctionPart> arguments)
    {
        Name = name.Trim(' ');
        Arguments = arguments;
    }

    public string Name { get; }
    public List<IFunctionPart> Arguments { get; }

    public TType Evaluate<TType>(RunState state)
    {
        if (!FunctionsRepository.Functions.TryGetValue(Name, out var function))
            throw new Exception($"Unsupported function: {Name}");

        var parameters = function.Method.GetParameters();
        var isParamsArgument = parameters.Length == 1 && parameters[0].ParameterType.IsGenericType && parameters[0].ParameterType.GetGenericTypeDefinition() == typeof(IEnumerable<>);

        if (!isParamsArgument && parameters.Length != Arguments.Count)
            throw new FunctionCallInvalidArgumentsCountException(Name, Arguments, parameters);

        var evaluatedArguments = Arguments.Select(argument =>
        {
            var argumentIndex = Arguments.IndexOf(argument);
            var parameterType = isParamsArgument ? parameters[0].ParameterType.GetGenericArguments()[0] : parameters[argumentIndex].ParameterType;

            return parameterType switch
            {
                { } when parameterType == typeof(string) => argument.Evaluate<string>(state),
                { } when parameterType == typeof(char) => argument.Evaluate<char>(state),
                { } when parameterType == typeof(bool) => argument.Evaluate<bool>(state),
                { } when parameterType == typeof(int) => argument.Evaluate<int>(state),
                { } when parameterType == typeof(long) => argument.Evaluate<long>(state),
                { } when parameterType == typeof(float) => argument.Evaluate<float>(state),
                { } when parameterType == typeof(double) => argument.Evaluate<double>(state),
                { } when parameterType == typeof(object) => argument.Evaluate<object>(state),
                { IsArray: true } => argument.Evaluate<object[]>(state),
                _ => throw new Exception($"Unsupported parameter type: {parameterType}")
            };
        }).ToList();

        try
        {
            var arguments = isParamsArgument ? TypeHelper.ConvertListGenericTypeToType(evaluatedArguments, parameters[0].ParameterType.GetGenericArguments()[0]) : evaluatedArguments;

            // Note: The following line's code duplication is a workaround to support functions with params arguments.
            return (TType)(isParamsArgument ? function.DynamicInvoke(arguments) : function.DynamicInvoke(evaluatedArguments.ToArray())) ?? throw new Exception($"Function {Name} returned null.");
        }
        catch (TargetParameterCountException)
        {
            throw new FunctionCallInvalidArgumentsCountException(Name, evaluatedArguments, parameters);
        }
    }
}