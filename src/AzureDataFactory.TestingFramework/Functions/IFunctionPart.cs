// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Models.Base;

namespace AzureDataFactory.TestingFramework.Functions;

public interface IFunctionPart
{
    public TType Evaluate<TType>(RunState state);
}