using System.Text.RegularExpressions;
using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Expressions;

/// <summary>
/// Used to evaluate any pipeline() expression, like pipeline().parameters.name and pipeline().globalParameters.name.
/// </summary>
public class ParameterExpression : BaseExpression, IRunExpression
{
    private readonly ParameterType _type;

    public ParameterExpression(string expression, ParameterType type) : base(expression)
    {
        _type = type;
    }

    public TType Evaluate<TType>(RunState state)
    {
        var parameterName = GetParameterName();
        return GetParameterValue<TType>(state, parameterName, _type);
    }

    private string GetParameterName()
    {
        var regex = "(@?{?pipeline\\(\\)\\." + GetParameterStringTemplate(_type) + @"\.(\w+)}?)";
        var match = Regex.Match(ExpressionValue, regex, RegexOptions.Singleline);
        if (match.Groups.Count != 3)
            throw new Exception();

        return match.Groups[2].Value;
    }

    private static string GetParameterStringTemplate(ParameterType type)
    {
        return type switch
        {
            ParameterType.Parameter => "parameters",
            ParameterType.Global => "globalParameters",
            _ => throw new NotImplementedException($"Parameter type {type} is not implemented.")
        };
    }

    public static IEnumerable<ParameterExpression> Find(string text,
        ParameterType parameterType)
    {
        var regex = "(@?{?pipeline\\(\\)\\." + GetParameterStringTemplate(parameterType) + @"\.(\w+)}?)";
        return ExpressionFinder.FindByRegex(text, regex, e => new ParameterExpression(e, parameterType));
    }

}