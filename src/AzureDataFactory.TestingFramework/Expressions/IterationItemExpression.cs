// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Expressions;

/// <summary>
/// Used to evaluate any item() expression.
/// </summary>
internal class IterationItemExpression : BaseExpression, IPipelineExpression
{
    private const string ExtractIterationItemRegex = "(@?{?item\\(\\)\\}?)";

    private IterationItemExpression(string expression) : base(expression)
    {
    }

    public TType Evaluate<TType>(PipelineRunState state)
    {
        if (typeof(TType) != typeof(string))
            throw new ArgumentException($"Only string is supported for {nameof(IterationItemExpression)}.");

        return (TType)(object)state.IterationItem;
    }

    public static IEnumerable<IterationItemExpression> Find(string text)
    {
        return ExpressionFinder.FindByRegex(text, ExtractIterationItemRegex, e => new IterationItemExpression(e));
    }
}