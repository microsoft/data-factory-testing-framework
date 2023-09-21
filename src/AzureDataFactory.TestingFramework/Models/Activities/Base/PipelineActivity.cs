// Copyright (c) Microsoft Corporation.

using System.Collections;
using Azure.Core.Expressions.DataFactory;
using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class PipelineActivity : DataFactoryEntity, IPipelineActivityResult
{
    public DependencyCondition? Status { get; protected set; }
    public object? Output { get; private set; }

    public PipelineActivity()
    {
    }

    public override DataFactoryEntity Evaluate(PipelineRunState state)
    {
        base.Evaluate(state);

        Status ??= DependencyCondition.Succeeded;

        return this;
    }

    public bool AreDependencyConditionMet(PipelineRunState state)
    {
        foreach (var dependency in DependsOn)
        {
            var dependencyActivity = state.ScopedPipelineActivityResults.SingleOrDefault(a => a.Name == dependency.Activity);

            // If dependency is not yet evaluated, conditions are not met
            if (dependencyActivity == null)
                return false;

            // If dependency is evaluated, but the result is not as expected, conditions are not met
            if (dependency.DependencyConditions.All(condition => condition != dependencyActivity.Status))
                return false;
        }

        return true;
    }

    public void SetResult<TResult>(DependencyCondition status, TResult output)
    {
        Status = status;
        Output = output;
    }
}