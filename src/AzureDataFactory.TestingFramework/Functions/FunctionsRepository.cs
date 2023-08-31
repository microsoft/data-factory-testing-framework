using System.Text.Json;
using System.Text.Json.Nodes;

namespace AzureDataFactory.TestingFramework.Functions;

public static class FunctionsRepository
{
    internal static readonly Dictionary<string, Delegate> Functions = new()
    {
        { "concat", (IEnumerable<string> arguments) => string.Concat(arguments) },
        { "trim", Trim },
        { "equals", FuncEquals },
        { "json", Json },
        { "contains", Contains },
        { "replace",  (string input, string pattern, string replacement) => input.Replace(pattern, replacement) },
        { "string", (string input) => input },
        { "union" , (string arg0, string arg1) => JsonSerializer.Serialize(JsonSerializer.Deserialize<JsonArray>(arg0).Union(JsonSerializer.Deserialize<JsonArray>((arg1)))) },
        { "coalesce", (IEnumerable<string> args) => args.FirstOrDefault(arg => !string.IsNullOrEmpty(arg)) }

    };

    public static void Register(string functionName, Delegate function)
    {
        Functions[functionName] = function;
    }

    private static object FuncEquals(string argument0, string argument1)
    {
        if (argument0.GetType() != argument1.GetType())
            throw new ArgumentException("Equals function requires arguments of the same type.");

        return argument0.Equals(argument1);
    }

    private static string Trim(string text, string trimArgument)
    {
        return text.Trim(trimArgument[0]);
    }

    private static string Json(string argument)
    {
        return argument;
    }

    private static bool Contains(object obj, string value)
    {
        if (obj is Dictionary<string, string> dictionary)
            return dictionary.ContainsKey(value);

        if (obj is IEnumerable<object> enumerable)
            return enumerable.Contains(value);

        if (obj is string text)
            return text.Contains(value);

        throw new ArgumentException("Contains function requires an object of type Dictionary, IEnumerable or string.");
    }
}