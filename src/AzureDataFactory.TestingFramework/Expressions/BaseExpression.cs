// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Expressions;

internal abstract class BaseExpression
{
    internal string ExpressionValue { get; }

    protected BaseExpression(string expressionValue)
    {
        ExpressionValue = expressionValue;
    }

    protected static TType GetParameterValue<TType>(RunState state, string parameterName, ParameterType parameterType)
    {
        var parameter = state.Parameters.SingleOrDefault(x => x.Name == parameterName && x.Type == parameterType);
        if (parameter == null)
            throw new ExpressionParameterNotFoundException(parameterName, parameterType);

        if (parameter is not RunParameter<TType> typedParameter)
            throw new ExpressionParameterOrVariableTypeMismatchException(parameterName, parameterType, typeof(TType));

        return typedParameter.Value;
    }
}

internal interface IPipelineExpression
{
    TType Evaluate<TType>(PipelineRunState state);
}

internal interface IRunExpression
{
    TType Evaluate<TType>(RunState state);
}