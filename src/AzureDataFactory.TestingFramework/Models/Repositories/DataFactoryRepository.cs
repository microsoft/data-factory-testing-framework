// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Azure.ResourceManager.DataFactory;
using AzureDataFactory.TestingFramework.Exceptions;

namespace AzureDataFactory.TestingFramework.Models.Repositories;

public class DataFactoryRepository
{
    /// <summary>
    /// Initializes the repository with pipelines, linkedServices, datasets and triggers which will be used to evaluate child entities upon pipeline evaluation
    /// </summary>
    /// <param name="pipelines">List of deserialized pipelines</param>
    /// <param name="linkedServices">List of deserialized linkedServices</param>
    /// <param name="datasets">List of deserialized datasets</param>
    /// <param name="triggers">List of deserialized triggers</param>
    public DataFactoryRepository(List<Pipeline> pipelines, List<DataFactoryLinkedServiceProperties> linkedServices, List<DataFactoryDatasetProperties> datasets, List<DataFactoryTriggerProperties> triggers)
    {
        Pipelines = pipelines;
        LinkedServices = linkedServices;
        Datasets = datasets;
        Triggers = triggers;
    }

    public DataFactoryRepository()
    {
        Pipelines = new List<Pipeline>();
        LinkedServices = new List<DataFactoryLinkedServiceProperties>();
        Datasets = new List<DataFactoryDatasetProperties>();
        Triggers = new List<DataFactoryTriggerProperties>();
    }

    public List<Pipeline> Pipelines { get; private set; }
    public List<DataFactoryLinkedServiceProperties> LinkedServices { get; private set; }
    public List<DataFactoryDatasetProperties> Datasets { get; private set; }
    public List<DataFactoryTriggerProperties> Triggers { get; private set; }

    public Pipeline GetPipelineByName(string name)
    {
        var pipeline = Pipelines.SingleOrDefault(pipeline => pipeline.Name == name);
        if (pipeline == null)
            throw new PipelineNotFoundException(name);

        return pipeline;
    }
}
