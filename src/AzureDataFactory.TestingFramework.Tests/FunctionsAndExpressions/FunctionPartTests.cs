// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests;

public class FunctionPartTests
{
    [Fact]
    public void ParseExpressionWithNestedFunctionAndSingleQuote()
    {
        // Arrange
        var state = new PipelineRunState();
        var rawExpression = "concat('https://example.com/jobs/', '123''', concat('&', 'abc,'))";

        // Act
        var expression = FunctionPart.Parse(rawExpression);

        // Assert
        var function = expression as FunctionCall;

        Assert.Equal(typeof(FunctionCall), expression.GetType());
        Assert.NotNull(function);
        Assert.Equal("concat", function.Name);
        Assert.Equal(3, function.Arguments.Count);
        Assert.Equal("'https://example.com/jobs/'", (function.Arguments[0] as FunctionArgument)?.ExpressionValue);
        Assert.Equal("'123''", (function.Arguments[1] as FunctionArgument)?.ExpressionValue);

        var innerFunction = function.Arguments[2] as FunctionCall;
        Assert.NotNull(innerFunction);
        Assert.Equal("concat", innerFunction.Name);
        Assert.Equal(2, innerFunction.Arguments.Count);
        Assert.Equal("'&'", (innerFunction.Arguments[0] as FunctionArgument)?.ExpressionValue);
        Assert.Equal("'abc,'", (innerFunction.Arguments[1] as FunctionArgument)?.ExpressionValue);
    }

    [Fact]
    public void ParseExpressionWithAdfNativeFunctions()
    {
        // Arrange
        var state = new PipelineRunState();
        var rawExpression = "concat('https://example.com/jobs/', '123''', variables('abc'), pipeline().parameters.abc, activity('abc').output.abc)";

        // Act
        var expression = FunctionPart.Parse(rawExpression);

        // Assert
        var function = expression as FunctionCall;
        Assert.Equal("concat", function.Name);
        Assert.Equal(5, function.Arguments.Count);
        Assert.Equal("'https://example.com/jobs/'", (function.Arguments[0] as FunctionArgument).ExpressionValue);
        Assert.Equal("'123''", (function.Arguments[1] as FunctionArgument).ExpressionValue);
        Assert.Equal("variables('abc')", (function.Arguments[2] as FunctionArgument).ExpressionValue);
        Assert.Equal("pipeline().parameters.abc", (function.Arguments[3] as FunctionArgument).ExpressionValue);
        Assert.Equal("activity('abc').output.abc", (function.Arguments[4] as FunctionArgument).ExpressionValue);
    }
}