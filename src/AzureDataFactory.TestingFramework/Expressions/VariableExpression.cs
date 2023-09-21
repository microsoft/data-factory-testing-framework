// Copyright (c) Microsoft Corporation.

using System.Text.RegularExpressions;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Expressions;

/// <summary>
/// Used to evaluate any variables('variableName') expression.
/// </summary>
internal class VariableExpression : BaseExpression, IPipelineExpression
{
    private const string ExtractVariablesRegex = @"(@?{?variables\('(\w+)'\)}?)";

    private VariableExpression(string expression) : base(expression)
    {
    }

    public TType Evaluate<TType>(PipelineRunState state)
    {
        var variableName = GetVariableName();
        return GetVariableValueFromState<TType>(state, variableName);
    }

    private string GetVariableName()
    {
        var match = Regex.Match(ExpressionValue, ExtractVariablesRegex, RegexOptions.Singleline);
        if (match.Groups.Count != 3)
            throw new Exception();

        return match.Groups[2].Value;
    }

    private static TType GetVariableValueFromState<TType>(PipelineRunState state, string variableName)
    {
        var parameter = state.Variables.SingleOrDefault(x => x.Name == variableName);
        if (parameter == null)
            throw new ExpressionParameterNotFoundException(variableName);

        if (parameter is not PipelineRunVariable<TType> typedParameter)
            throw new ExpressionParameterOrVariableTypeMismatchException(variableName, typeof(TType));

        return typedParameter.Value;
    }

    public static IEnumerable<VariableExpression> Find(string text)
    {
        return ExpressionFinder.FindByRegex(text, ExtractVariablesRegex, e => new VariableExpression(e));
    }
}