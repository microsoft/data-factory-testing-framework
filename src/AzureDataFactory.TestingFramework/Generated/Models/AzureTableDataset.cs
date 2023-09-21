// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> The Azure Table storage dataset. </summary>
    public partial class AzureTableDataset : DataFactoryDatasetProperties
    {
        /// <summary> Initializes a new instance of AzureTableDataset. </summary>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <param name="tableName"> The table name of the Azure Table storage. Type: string (or Expression with resultType string). </param>
        /// <exception cref="ArgumentNullException"> <paramref name="linkedServiceName"/> or <paramref name="tableName"/> is null. </exception>
        public AzureTableDataset(DataFactoryLinkedServiceReference linkedServiceName, DataFactoryElement<string> tableName) : base(linkedServiceName)
        {
            Argument.AssertNotNull(linkedServiceName, nameof(linkedServiceName));
            Argument.AssertNotNull(tableName, nameof(tableName));

            TableName = tableName;
            DatasetType = "AzureTable";
        }

        /// <summary> Initializes a new instance of AzureTableDataset. </summary>
        /// <param name="datasetType"> Type of dataset. </param>
        /// <param name="description"> Dataset description. </param>
        /// <param name="structure"> Columns that define the structure of the dataset. Type: array (or Expression with resultType array), itemType: DatasetDataElement. </param>
        /// <param name="schema"> Columns that define the physical type schema of the dataset. Type: array (or Expression with resultType array), itemType: DatasetSchemaDataElement. </param>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <param name="parameters"> Parameters for dataset. </param>
        /// <param name="annotations"> List of tags that can be used for describing the Dataset. </param>
        /// <param name="folder"> The folder that this Dataset is in. If not specified, Dataset will appear at the root level. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="tableName"> The table name of the Azure Table storage. Type: string (or Expression with resultType string). </param>
        internal AzureTableDataset(string datasetType, string description, DataFactoryElement<IList<DatasetDataElement>> structure, DataFactoryElement<IList<DatasetSchemaDataElement>> schema, DataFactoryLinkedServiceReference linkedServiceName, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, DatasetFolder folder, IDictionary<string, DataFactoryElement<string>> additionalProperties, DataFactoryElement<string> tableName) : base(datasetType, description, structure, schema, linkedServiceName, parameters, annotations, folder, additionalProperties)
        {
            TableName = tableName;
            DatasetType = datasetType ?? "AzureTable";
        }

        /// <summary> The table name of the Azure Table storage. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> TableName { get; set; }
    }
}
