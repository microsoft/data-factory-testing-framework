using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Expressions;
using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests;

public class FunctionArgumentTests
{
    private readonly PipelineRunState _state;

    public FunctionArgumentTests()
    {
        _state = new PipelineRunState();
    }

    [Fact]
    private void EvaluateVariableStringExpression()
    {
        // Arrange
        var expression = "variables('variableName')";
        var argument = new FunctionArgument(expression);
        _state.Variables.Add(new PipelineRunVariable<string>("variableName", "variableValue"));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("variableValue", evaluated);
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    private void EvaluateVariableBoolExpression(bool boolValue)
    {
        // Arrange
        var expression = "variables('variableName')";
        var argument = new FunctionArgument(expression);
        _state.Variables.Add(new PipelineRunVariable<bool>("variableName", boolValue));

        // Act
        var evaluated = argument.Evaluate<bool>(_state);

        // Assert
        Assert.Equal(boolValue, evaluated);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(2)]
    private void EvaluateVariableIntExpression(int intValue)
    {
        // Arrange
        var expression = "variables('variableName')";
        var argument = new FunctionArgument(expression);
        _state.Variables.Add(new PipelineRunVariable<int>("variableName", intValue));

        // Act
        var evaluated = argument.Evaluate<int>(_state);

        // Assert
        Assert.Equal(intValue, evaluated);
    }

    [Fact]
    private void EvaluateParameterExpression()
    {
        // Arrange
        var expression = "pipeline().parameters.parameterName";
        var argument = new FunctionArgument(expression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "parameterName", "parameterValue"));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("parameterValue", evaluated);
    }

    [Fact]
    private void EvaluateGlobalParameterExpression()
    {
        // Arrange
        var expression = "pipeline().globalParameters.parameterName";
        var argument = new FunctionArgument(expression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "parameterName", "parameterValue"));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("parameterValue", evaluated);
    }

    [Fact]
    private void EvaluateActivityOutputExpression()
    {
        // Arrange
        var expression = "activity('activityName').output.outputName";
        var argument = new FunctionArgument(expression);
        _state.AddActivityResult(new TestActivityResult("activityName", new { outputName = "outputValue" }));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("outputValue", evaluated);
    }

    [Fact]
    private void EvaluateIterationExpression()
    {
        // Arrange
        var expression = "item()";
        var argument = new FunctionArgument(expression);
        _state.IterationItem = "item0";

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("item0", evaluated);
    }

    [Fact]
    private void EvaluateDatasetExpression()
    {
        // Arrange
        var expression = "dataset().datasetParameter";
        var argument = new FunctionArgument(expression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Dataset, "datasetParameter", "datasetValue"));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("datasetValue", evaluated);
    }

    [Fact]
    private void EvaluateLinkedServiceExpression()
    {
        // Arrange
        var expression = "linkedService().linkedServiceParameter";
        var argument = new FunctionArgument(expression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.LinkedService, "linkedServiceParameter", "linkedServiceValue"));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("linkedServiceValue", evaluated);
    }

    [Fact]
    private void EvaluateParameterInString()
    {
        // Arrange
        var expression = "{ \"parameter\": \"@pipeline().parameters.parameterName\" }";
        var argument = new FunctionArgument(expression);
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "parameterName", "parameterValue"));

        // Act
        var evaluated = argument.Evaluate<string>(_state);

        // Assert
        Assert.Equal("{ \"parameter\": \"parameterValue\" }", evaluated);
    }

    [Fact]
    public void EvaluateUnknownParameter()
    {
        // Arrange
        var expression = "pipeline().parameters.parameterName";
        var argument = new FunctionArgument(expression);

        // Act
        Assert.Throws<ExpressionParameterNotFoundException>(() => argument.Evaluate<string>(_state));
    }

    [Fact]
    public void EvaluateUnknownVariable()
    {
        // Arrange
        var expression = "variables('variableName')";
        var argument = new FunctionArgument(expression);

        // Act
        Assert.Throws<ExpressionParameterNotFoundException>(() => argument.Evaluate<string>(_state));
    }

    [Fact]
    public void EvaluateUnknownActivity()
    {
        // Arrange
        var expression = "activity('activityName').output.outputName";
        var argument = new FunctionArgument(expression);

        // Act
        Assert.Throws<ActivityNotFoundException>(() => argument.Evaluate<string>(_state));
    }

    [Fact]
    public void EvaluateUnknownDataset()
    {
        // Arrange
        var expression = "dataset().datasetParameter";
        var argument = new FunctionArgument(expression);

        // Act
        Assert.Throws<ExpressionParameterNotFoundException>(() => argument.Evaluate<string>(_state));
    }

    [Fact]
    public void EvaluateUnknownLinkedService()
    {
        // Arrange
        var expression = "linkedService().linkedServiceParameter";
        var argument = new FunctionArgument(expression);

        // Act
        Assert.Throws<ExpressionParameterNotFoundException>(() => argument.Evaluate<string>(_state));
    }

    [Fact]
    public void EvaluateParameterOfWrongType()
    {
        // Arrange
        var expression = "pipeline().parameters.parameterName";
        var argument = new FunctionArgument(expression);
        _state.Parameters.Add(new RunParameter<int>(ParameterType.Parameter, "parameterName", 1));

        // Act
        Assert.Throws<ExpressionParameterOrVariableTypeMismatchException>(() => argument.Evaluate<string>(_state));
    }
}