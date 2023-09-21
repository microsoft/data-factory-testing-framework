// Copyright (c) Microsoft Corporation.

namespace AzureDataFactory.TestingFramework.Models.Base;

public class RunState
{
    public RunState(List<IRunParameter> parameters)
    {
        Parameters = parameters;
    }

    public List<IRunParameter> Parameters { get; }
}