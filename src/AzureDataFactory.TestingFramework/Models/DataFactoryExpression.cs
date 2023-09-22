// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class DataFactoryExpression
{
    /// <summary>
    /// Evaluates the expression by replacing all parameters and variables with their values and then evaluating the expression.
    /// </summary>
    /// <param name="state">The pipeline state to be used for evaluating the expressions.</param>
    /// <typeparam name="TType">The type of the expression result. Can be string, bool, int and long.</typeparam>
    /// <returns>The evaluated result of the expression.</returns>
    public TType Evaluate<TType>(PipelineRunState state)
    {
        return FunctionPart.Parse(Value).Evaluate<TType>(state);
    }
}