// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Activities.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class ControlActivity
{
    internal delegate IEnumerable<PipelineActivity> EvaluateActivitiesDelegate(List<PipelineActivity> activities, PipelineRunState state);
    internal virtual IEnumerable<PipelineActivity> EvaluateControlActivityIterations(PipelineRunState state,  EvaluateActivitiesDelegate evaluateActivities)
    {
        // Note: unfortunately cannot use abstract method
        return new List<PipelineActivity>();
    }
}