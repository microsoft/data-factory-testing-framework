// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Functions;

public interface IFunctionPart
{
    public TType Evaluate<TType>(RunState state);
}