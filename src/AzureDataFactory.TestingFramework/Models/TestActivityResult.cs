// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Activities.Base;

namespace AzureDataFactory.TestingFramework;

public class TestActivityResult : IPipelineActivityResult
{
    public string Name { get; }
    public DependencyCondition? Status { get; }
    public object Output { get; }

    public TestActivityResult(string name)
    {
        Name = name;
        Status = DependencyCondition.Succeeded;
        Output = new Dictionary<string, object>();
    }

    public TestActivityResult(string name, object output)
    {
        Name = name;
        Status = DependencyCondition.Succeeded;
        Output = output;
    }

    public TestActivityResult(string name, DependencyCondition status)
    {
        Name = name;
        Status = status;
        Output = new Dictionary<string, object>();
    }
}