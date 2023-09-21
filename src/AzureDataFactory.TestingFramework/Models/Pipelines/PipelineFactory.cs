// Copyright (c) Microsoft Corporation.

using System.Text.Json;
using Azure.ResourceManager.DataFactory;

namespace AzureDataFactory.TestingFramework.Models.Pipelines;

public static class PipelineFactory
{
    /// <summary>
    /// Parses the pipeline entity from a file.
    /// </summary>
    /// <param name="pipelineResourceJson">The path to the resource json file</param>
    /// <returns>A deserialized pipeline that can be evaluated for assertions</returns>
    public static Pipeline ParseFromFile(string pipelineResourceJson)
    {
        var pipelineJson = File.ReadAllText(pipelineResourceJson);
        var pipelineJsonElement = JsonSerializer.Deserialize<JsonElement>(pipelineJson);
        return Pipeline.DeserializeDataFactoryPipelineData(pipelineJsonElement);
    }
}