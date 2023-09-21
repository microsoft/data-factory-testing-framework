// Copyright (c) Microsoft Corporation.

using System.Text.RegularExpressions;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Expressions;

/// <summary>
/// Used to evaluate any activity('activityName').status or activity('activityName').output.field1.field2
/// </summary>
internal class ActivityExpression : BaseExpression, IPipelineExpression
{
    private const string ExtractActivityRegex = @"(@?{?activity\('(\w+( +\w+)*)'\)(\.(\w+))*}?)";

    private ActivityExpression(string expression) : base(expression)
    {
    }

    public TType Evaluate<TType>(PipelineRunState state)
    {
        var (activityName, fields) = GetActivityNameAndFields();
        var activity = state.PipelineActivityResults.LastOrDefault(x => string.Equals(x.Name, activityName, StringComparison.CurrentCultureIgnoreCase)) ??
                       throw new ActivityNotFoundException(activityName);
        if (activity.Status == null)
            throw new ActivityNotEvaluatedException(activity.Name);

        var firstField = fields[0];
        switch (firstField)
        {
            case "status":
                if (typeof(TType) != typeof(string))
                    throw new TypeOfPipelineActivityResultDoesNotMatchExpectedType(activity.Name, firstField, typeof(string), typeof(TType));

                return (TType)(object)activity.Status.ToString().ToLower();
            case "output":
                var activityOutput = activity.Output;
                foreach (var field in fields.Skip(1))
                {
                    // Use reflection to get field on activityOutput
                    var property = activityOutput.GetType().GetProperty(field);
                    if (property == null)
                        throw new ActivityOutputFieldNotFoundException(activity.Name, field);

                    activityOutput = property.GetValue(activityOutput) ?? throw new ActivityOutputFieldNotFoundException(activity.Name, field);
                }

                if (activityOutput is not TType type)
                    throw new TypeOfPipelineActivityResultDoesNotMatchExpectedType(activity.Name, string.Join(".", fields), activityOutput.GetType(), typeof(TType));

                return type;
            default:
                throw new ActivityOutputFieldNotFoundException(activity.Name, firstField);
        }
    }

    private (string ActivityName, IReadOnlyList<string> Fields) GetActivityNameAndFields()
    {
        var match = Regex.Match(ExpressionValue, ExtractActivityRegex, RegexOptions.Singleline);
        if (match.Groups.Count != 6)
            throw new Exception();

        var activityName = match.Groups[2].Value;
        var fields = match.Groups[5].Captures.Select(x => x.Value).ToList();

        return (activityName, fields);
    }

    internal static IEnumerable<ActivityExpression> Find(string text)
    {
        return ExpressionFinder.FindByRegex(text, ExtractActivityRegex, e => new ActivityExpression(e));
    }
}