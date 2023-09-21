// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Extensions;

public static class StringExtensions
{
    public static string TrimOneChar(this string text, char character)
    {
        text = text.StartsWith(character) ? text[1..] : text;
        text = text.EndsWith(character) ? text[..^1] : text;
        return text;
    }
}