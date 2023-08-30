using System.Text.RegularExpressions;

namespace AzureDataFactory.TestingFramework.Expressions;

public static class ExpressionFinder
{
    public static IReadOnlyList<TExpression> FindByRegex<TExpression>(string text, string regex, Func<string, TExpression> expressionFactory) where TExpression : BaseExpression
    {
        var matches = Regex.Matches(text, regex, RegexOptions.Singleline);
        return matches.Select(x => x.Value).Select(expressionFactory).ToList();
    }
}