using System.Text.RegularExpressions;

namespace AzureDataFactory.TestingFramework.Functions;

public static class FunctionPart
{
    private const string ExtractFuncRegex = @"^@?{?([^()]+?)\((.*)\)}?$";

    public static IFunctionPart Parse(string expression)
    {
        var match = Regex.Match(expression, ExtractFuncRegex, RegexOptions.Singleline);
        if (match.Groups.Count != 3)
            return new FunctionArgument(expression);

        var functionName = match.Groups[1].Value.Trim();
        if (functionName is "variables" or "activity" or "pipeline")
            return new FunctionArgument(expression);

        var functionArgumentsExpression = match.Groups[2].Value;

        var start = 0;
        var inQuotes = false;
        var inParenthesis = 0;
        var arguments = new List<string>();
        for (int i = 0; i < functionArgumentsExpression.Length; i++)
        {
            var currentChar = functionArgumentsExpression[i];
            var nextChar = i < functionArgumentsExpression.Length - 1 ? functionArgumentsExpression[i + 1] : '\0';
            if (currentChar == ',' && !inQuotes && inParenthesis == 0)
            {
                arguments.Add(functionArgumentsExpression[start..i].Replace("''", "'"));
                start = i + 1;
                continue;
            }

            // Skip escaped single quotes
            if (inQuotes && currentChar == '\'' && nextChar == '\'')
            {
                i++;
                continue;
            }

            if (currentChar == '\'')
                inQuotes = !inQuotes;

            if (currentChar == '(')
                inParenthesis++;

            if (currentChar == ')')
                inParenthesis--;

            if (i == functionArgumentsExpression.Length - 1)
                arguments.Add(functionArgumentsExpression[start..(i + 1)].Replace("''", "'"));
        }

        return new FunctionCall(
            functionName,
            arguments.Select(x => x.Trim()).Select(Parse).ToList()
        );
    }

    // This Parsing method is neat, however regex must be adapted to handle comma's and escaped quotes in strings .
    //
    // private const string ExtractArgsRegex = @"(?:[^,()]+((?:\((?>[^()]+|\((?<open>)|\)(?<-open>))*\)))*)+";
    // public static IFunctionPart ParseByRegex(string expression)
    // {
    //     var match = Regex.Match(expression, ExtractFuncRegex, RegexOptions.Singleline);
    //     if (match.Groups.Count != 3)
    //         return new FunctionArgument(expression);
    //
    //     var functionName = match.Groups[1].Value.Trim();
    //     if (functionName is "variables" or "activity" or "pipeline")
    //         return new FunctionArgument(expression);
    //
    //     var functionArgumentsExpression = match.Groups[2].Value;
    //     var functionArguments = Regex.Matches(functionArgumentsExpression, ExtractArgsRegex);
    //
    //     return new FunctionCall(
    //         functionName,
    //         functionArguments.Select(x => x.Value).Select(Parse).ToList()
    //     );
    // }
}