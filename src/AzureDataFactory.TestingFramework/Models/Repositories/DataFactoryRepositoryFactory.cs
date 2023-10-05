// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using System.Text.Json;
using Azure.ResourceManager.DataFactory;

namespace AzureDataFactory.TestingFramework.Models.Repositories;

public static class DataFactoryRepositoryFactory
{
    public static DataFactoryRepository ParseFromFolder(string folderPath)
    {
        var pipelines = GetDataFactoryEntitiesByFolderPath(Path.Combine(folderPath, "pipeline"), Pipeline.DeserializeDataFactoryPipelineData);
        var linkedServices = GetDataFactoryEntitiesByFolderPath(Path.Combine(folderPath, "linkedService"), DataFactoryLinkedServiceData.DeserializeDataFactoryLinkedServiceData);
        var datasets = GetDataFactoryEntitiesByFolderPath(Path.Combine(folderPath, "dataset"), DataFactoryDatasetData.DeserializeDataFactoryDatasetData);
        var triggers = GetDataFactoryEntitiesByFolderPath(Path.Combine(folderPath, "trigger"), DataFactoryTriggerData.DeserializeDataFactoryTriggerData);

        return new DataFactoryRepository(pipelines, linkedServices, datasets, triggers);
    }

    private static List<TType> GetDataFactoryEntitiesByFolderPath<TType>(string folderPath, Func<JsonElement, TType> deserialize) where TType : class
    {
        if (!Directory.Exists(folderPath))
            return new List<TType>();

        return Directory.GetFiles(folderPath, "*.json")
            .Select(File.ReadAllText)
            .Select(json => JsonSerializer.Deserialize<JsonElement>(json))
            .Select(deserialize)
            .ToList();
    }
}
