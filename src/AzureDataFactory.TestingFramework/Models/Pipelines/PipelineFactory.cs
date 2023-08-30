using System.Text.Json;
using Azure.ResourceManager.DataFactory;

namespace AzureDataFactory.TestingFramework.Models.Pipelines;

public static class PipelineFactory
{
    public static Pipeline ParseFromFile(string pipelineResourceJson)
    {
        var pipelineJson = File.ReadAllText(pipelineResourceJson);
        var pipelineJsonElement = JsonSerializer.Deserialize<JsonElement>(pipelineJson);
        return Pipeline.DeserializeDataFactoryPipelineData(pipelineJsonElement);
    }
}