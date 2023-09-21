// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Activities.Base;

namespace AzureDataFactory.TestingFramework;

public class TestActivityResult : IPipelineActivityResult
{
    public string Name { get; }
    public DependencyCondition? Status { get; }
    public object Output { get; }

    /// <summary>
    /// Initializes a new instance of the <see cref="TestActivityResult"/> class with a default status of Succeeded.
    /// </summary>
    /// <param name="name">Name of the activity being represented</param>
    public TestActivityResult(string name)
    {
        Name = name;
        Status = DependencyCondition.Succeeded;
        Output = new Dictionary<string, object>();
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="TestActivityResult"/> class with a default status of Succeeded.
    /// </summary>
    /// <param name="name">Name of the activity being represented</param>
    /// <param name="output">The output of the activity which will be used when referred to from other activities</param>
    public TestActivityResult(string name, object output)
    {
        Name = name;
        Status = DependencyCondition.Succeeded;
        Output = output;
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="TestActivityResult"/> class.
    /// </summary>
    /// <param name="name">Name of the activity being represented</param>
    /// <param name="status">The status outcome of the activity, which will be used to determine execution eligibility of other activities.</param>
    public TestActivityResult(string name, DependencyCondition status)
    {
        Name = name;
        Status = status;
        Output = new Dictionary<string, object>();
    }
}