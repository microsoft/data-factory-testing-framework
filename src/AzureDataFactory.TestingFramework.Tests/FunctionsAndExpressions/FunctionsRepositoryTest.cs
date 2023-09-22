// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests;

public class FunctionsRepositoryTest
{
    [Fact]
    public void RegisterMultiplicationFunctionTest()
    {
        // Arrange
        FunctionsRepository.Register("multiply", (int arg0, int arg1) => arg0 * arg1);
        var expression = "multiply(7, 6)";
        var functionPart = FunctionPart.Parse(expression);

        // Act
        var evaluated = functionPart.Evaluate<int>(new PipelineRunState());

        // Assert
        Assert.Equal(42, evaluated);
    }
}