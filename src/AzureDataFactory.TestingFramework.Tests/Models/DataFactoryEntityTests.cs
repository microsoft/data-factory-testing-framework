// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models;
using Azure.Core.Expressions.DataFactory;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Tests.Models;

public class DataFactoryEntityTests
{
    [Fact]
    public void WhenEvaluatingEntity_ShouldEvaluateAllProperties()
    {
        // Arrange
        var entity = new WebActivity("TestActivity", WebActivityMethod.Get, new DataFactoryElement<string>("@concat('https://example.com', '/123')", DataFactoryElementKind.Expression));

        // Act
        entity.Evaluate(new PipelineRunState());

        // Assert
        Assert.NotNull(entity);
        Assert.Equal("https://example.com/123", entity.Uri);
    }

    [Fact]
    public void WhenNotEvaluatingEntity_ShouldNotEvaluateAllProperties()
    {
        // Arrange
        var entity = new WebActivity("TestActivity", WebActivityMethod.Get, new DataFactoryElement<string>("@concat('https://example.com', '/123')", DataFactoryElementKind.Expression));

        // Act

        // Assert
        Assert.NotNull(entity);
        Assert.Throws<ExpressionNotEvaluatedException>(() => entity.Uri.Value);
    }
}