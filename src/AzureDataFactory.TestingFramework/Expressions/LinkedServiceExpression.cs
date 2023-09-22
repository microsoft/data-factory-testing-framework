// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using System.Text.RegularExpressions;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Expressions;

/// <summary>
/// Used to evaluate any linkedService('linkedServiceName') expression.
/// </summary>
internal class LinkedServiceExpression : BaseExpression, IRunExpression
{
    private const string ExtractLinkedServiceRegex = @"(@?{?linkedService\(\)\.(\w+)}?)";

    private LinkedServiceExpression(string expression) : base(expression)
    {
    }

    public TType Evaluate<TType>(RunState state)
    {
        var parameterName = GetParameterName();
        return GetParameterValue<TType>(state, parameterName, ParameterType.LinkedService);
    }

    private string GetParameterName()
    {
        var match = Regex.Match(ExpressionValue, ExtractLinkedServiceRegex, RegexOptions.Singleline);
        if (match.Groups.Count != 3)
            throw new Exception();

        return match.Groups[2].Value;
    }

    public static IEnumerable<LinkedServiceExpression> Find(string text)
    {
        return ExpressionFinder.FindByRegex(text, ExtractLinkedServiceRegex, e => new LinkedServiceExpression(e));
    }
}