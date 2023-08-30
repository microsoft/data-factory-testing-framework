using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;
using Xunit.Sdk;

namespace AzureDataFactory.TestingFramework.Tests;

public class FunctionCallTests
{
    private PipelineRunState _state;

    public FunctionCallTests()
    {
        _state = new PipelineRunState();
    }

    [Fact]
    private void EvaluateExpressionWithNestedFunction()
    {
        var rawExpression = "concat('https://example.com/jobs/,', '123''', concat('&', 'abc,'))";
        var expression = FunctionPart.Parse(rawExpression);

        var evaluated = expression.Evaluate<string>(new PipelineRunState());

        Assert.Equal("https://example.com/jobs/,123'&abc,", evaluated);
    }

    [Fact]
    private void EvaluateWithParameter()
    {
        // Arrange
        var rawExpression = "concat('https://example.com/jobs/', pipeline().parameters.abc)";
        var expression = FunctionPart.Parse(rawExpression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "abc", "123"));

        // Act
        var evaluated = expression.Evaluate<string>(_state);

        // Assert
        Assert.Equal("https://example.com/jobs/123", evaluated);
    }

    [Fact]
    private void EvaluateWithGlobalParameter()
    {
        // Arrange
        var rawExpression = "concat('https://example.com/jobs/', pipeline().globalParameters.abc)";
        var expression = FunctionPart.Parse(rawExpression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "abc", "123"));

        // Act
        var evaluated = expression.Evaluate<string>(_state);

        // Assert
        Assert.Equal("https://example.com/jobs/123", evaluated);
    }

    [Fact]
    private void EvaluateWithVariable()
    {
        // Arrange
        var rawExpression = "concat('https://example.com/jobs/', variables('abc'))";
        var expression = FunctionPart.Parse(rawExpression);
        _state.Variables.Add(new PipelineRunVariable<string>("abc", "123"));

        // Act
        var evaluated = expression.Evaluate<string>(_state);

        // Assert
        Assert.Equal("https://example.com/jobs/123", evaluated);
    }

    [Fact]
    private void EvaluateWithActivityOutput()
    {
        // Arrange
        var rawExpression = "concat('https://example.com/jobs/', activity('abc').output.abc)";
        var expression = FunctionPart.Parse(rawExpression);
        _state.AddActivityResult(new TestActivityResult("abc", new { abc = "123" }));

        // Act
        var evaluated = expression.Evaluate<string>(_state);

        // Assert
        Assert.Equal("https://example.com/jobs/123", evaluated);
    }

    [Fact]
    private void EvaluateWithActivityOutputAndVariable()
    {
        // Arrange
        var rawExpression = "concat('https://example.com/jobs/', activity('abc').output.abc, '/', variables('abc'))";
        var expression = FunctionPart.Parse(rawExpression);
        _state.AddActivityResult(new TestActivityResult("abc", new { abc = "123" }));
        _state.Variables.Add(new PipelineRunVariable<string>("abc", "456"));

        // Act
        var evaluated = expression.Evaluate<string>(_state);

        // Assert
        Assert.Equal("https://example.com/jobs/123/456", evaluated);
    }

    [Fact]
    private void EvaluateWithActivityOutputAndVariableAndParameters()
    {
        // Arrange
        var rawExpression = "concat('https://example.com/jobs/', activity('abc').output.abc, '/', variables('abc'), '/', pipeline().parameters.abc, '/', pipeline().globalParameters.abc)";
        var expression = FunctionPart.Parse(rawExpression);
        _state.AddActivityResult(new TestActivityResult("abc", new { abc = "123" }));
        _state.Variables.Add(new PipelineRunVariable<string>("abc", "456"));
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "abc", "789"));
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "abc", "10"));

        // Act
        var evaluated = expression.Evaluate<string>(_state);

        // Assert
        Assert.Equal("https://example.com/jobs/123/456/789/10", evaluated);
    }

    [Theory]
    [InlineData("'abc'", "'abc'", true)]
    [InlineData("'abc'", "'abc1'", false)]
    [InlineData("1", "1", true)]
    [InlineData("1", "2", false)]
    private void EvaluateEqualsExpression(string left, string right, bool expected)
    {
        // Arrange
        var rawExpression = $"equals({left}, {right})";
        var expression = FunctionPart.Parse(rawExpression);

        // Act
        var evaluated =
            expression.Evaluate<bool>(new PipelineRunState());

        Assert.Equal(expected, evaluated);
    }

    [Theory]
    [InlineData(1, 1, true)]
    [InlineData(1, 2, false)]
    [InlineData(2, 2, true)]
    [InlineData(0, -1, false)]
    private void EvaluateEqualsIntExpression(int left, int right, bool expected)
    {
        // Arrange
        var rawExpression = $"equals({left}, {right})";
        var expression = FunctionPart.Parse(rawExpression);

        // Act
        var evaluated =
            expression.Evaluate<bool>(new PipelineRunState());

        Assert.Equal(expected, evaluated);
    }

    [Theory]
    [InlineData("SomeKey", true)]
    [InlineData("SomeKey2", true)]
    [InlineData("SomeKey3", false)]
    public void ContainsDictionaryKeyExpression(string key, bool expected)
    {
        // Arrange
        var state = new PipelineRunState();
        state.AddActivityResult(new TestActivityResult("someActivityOutputingDictionary", new
        {
            SomeDictionary = new Dictionary<string, string>()
            {
                { "SomeKey", "SomeValue" },
                { "SomeKey2", "SomeValue2" }
            }
        }));

        var rawExpression = $"@contains(activity('someActivityOutputingDictionary').output.SomeDictionary, '{key}')";
        var expression = FunctionPart.Parse(rawExpression);

        // Act
        var evaluated = expression.Evaluate<bool>(state);

        // Assert
        Assert.Equal(expected, evaluated);
    }

    [Theory]
    [InlineData("SomeItem", true)]
    [InlineData("SomeItem2", true)]
    [InlineData("SomeItem3", false)]
    public void ContainsListItemExpression(string key, bool expected)
    {
        // Arrange
        var state = new PipelineRunState();
        state.AddActivityResult(new TestActivityResult("someActivityOutputingList", new
        {
            SomeList = new List<string>()
            {
                "SomeItem",
                "SomeItem2"
            }
        }));

        var rawExpression = $"@contains(activity('someActivityOutputingList').output.SomeList, '{key}')";
        var expression = FunctionPart.Parse(rawExpression);

        // Act
        var evaluated = expression.Evaluate<bool>(state);

        // Assert
        Assert.Equal(expected, evaluated);
    }

    [Theory]
    [InlineData("PartOfString", true)]
    [InlineData("NotPartOfString", false)]
    public void ContainsStringExpression(string substring, bool expected)
    {
        // Arrange
        var state = new PipelineRunState();
        state.AddActivityResult(new TestActivityResult("someActivityOutputingString", new {
            SomeString = "A message that contains PartOfString!"
        }));

        var rawExpression = $"@contains(activity('someActivityOutputingString').output.SomeString, '{substring}')";
        var expression = FunctionPart.Parse(rawExpression);

        // Act
        var evaluated = expression.Evaluate<bool>(state);

        // Assert
        Assert.Equal(expected, evaluated);
    }

    [Fact]
    public void EqualsIncorrectParameterCountThrowsException()
    {
        // Arrange
        var rawExpression = $"equals('1', '2', '3')";
        var expression = FunctionPart.Parse(rawExpression);

        // Act
        Assert.Throws<FunctionCallInvalidArgumentsCountException>(() => expression.Evaluate<bool>(new PipelineRunState()));
    }
}