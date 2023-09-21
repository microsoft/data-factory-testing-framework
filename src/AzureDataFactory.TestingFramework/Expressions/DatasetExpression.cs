// Copyright (c) Microsoft Corporation.

using System.Text.RegularExpressions;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Expressions;

/// <summary>
/// Used to evaluate any dataset('datasetName') expression.
/// </summary>
internal class DatasetExpression : BaseExpression, IRunExpression
{
    private const string ExtractDatasetRegex = @"(@?{?dataset\(\)\.(\w+)}?)";

    private DatasetExpression(string expression) : base(expression)
    {
    }

    public TType Evaluate<TType>(RunState state)
    {
        var parameterName = GetParameterName();
        return GetParameterValue<TType>(state, parameterName, ParameterType.Dataset);
    }

    private string GetParameterName()
    {
        var match = Regex.Match(ExpressionValue, ExtractDatasetRegex, RegexOptions.Singleline);
        if (match.Groups.Count != 3)
            throw new Exception();

        return match.Groups[2].Value;
    }

    public static IEnumerable<DatasetExpression> Find(string text)
    {
        return ExpressionFinder.FindByRegex(text, ExtractDatasetRegex, e => new DatasetExpression(e));
    }
}