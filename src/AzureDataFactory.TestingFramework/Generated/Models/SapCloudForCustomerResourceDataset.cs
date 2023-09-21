// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> The path of the SAP Cloud for Customer OData entity. </summary>
    public partial class SapCloudForCustomerResourceDataset : DataFactoryDatasetProperties
    {
        /// <summary> Initializes a new instance of SapCloudForCustomerResourceDataset. </summary>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <param name="path"> The path of the SAP Cloud for Customer OData entity. Type: string (or Expression with resultType string). </param>
        /// <exception cref="ArgumentNullException"> <paramref name="linkedServiceName"/> or <paramref name="path"/> is null. </exception>
        public SapCloudForCustomerResourceDataset(DataFactoryLinkedServiceReference linkedServiceName, DataFactoryElement<string> path) : base(linkedServiceName)
        {
            Argument.AssertNotNull(linkedServiceName, nameof(linkedServiceName));
            Argument.AssertNotNull(path, nameof(path));

            Path = path;
            DatasetType = "SapCloudForCustomerResource";
        }

        /// <summary> Initializes a new instance of SapCloudForCustomerResourceDataset. </summary>
        /// <param name="datasetType"> Type of dataset. </param>
        /// <param name="description"> Dataset description. </param>
        /// <param name="structure"> Columns that define the structure of the dataset. Type: array (or Expression with resultType array), itemType: DatasetDataElement. </param>
        /// <param name="schema"> Columns that define the physical type schema of the dataset. Type: array (or Expression with resultType array), itemType: DatasetSchemaDataElement. </param>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <param name="parameters"> Parameters for dataset. </param>
        /// <param name="annotations"> List of tags that can be used for describing the Dataset. </param>
        /// <param name="folder"> The folder that this Dataset is in. If not specified, Dataset will appear at the root level. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="path"> The path of the SAP Cloud for Customer OData entity. Type: string (or Expression with resultType string). </param>
        internal SapCloudForCustomerResourceDataset(string datasetType, string description, DataFactoryElement<IList<DatasetDataElement>> structure, DataFactoryElement<IList<DatasetSchemaDataElement>> schema, DataFactoryLinkedServiceReference linkedServiceName, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, DatasetFolder folder, IDictionary<string, DataFactoryElement<string>> additionalProperties, DataFactoryElement<string> path) : base(datasetType, description, structure, schema, linkedServiceName, parameters, annotations, folder, additionalProperties)
        {
            Path = path;
            DatasetType = datasetType ?? "SapCloudForCustomerResource";
        }

        /// <summary> The path of the SAP Cloud for Customer OData entity. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> Path { get; set; }
    }
}
