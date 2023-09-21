// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Extensions;

internal static class StringExtensions
{
    internal static string TrimOneChar(this string text, char character)
    {
        text = text.StartsWith(character) ? text[1..] : text;
        text = text.EndsWith(character) ? text[..^1] : text;
        return text;
    }
}