// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> A file in an HTTP web server. </summary>
    public partial class DataFactoryHttpDataset : DataFactoryDatasetProperties
    {
        /// <summary> Initializes a new instance of DataFactoryHttpDataset. </summary>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="linkedServiceName"/> is null. </exception>
        public DataFactoryHttpDataset(DataFactoryLinkedServiceReference linkedServiceName) : base(linkedServiceName)
        {
            Argument.AssertNotNull(linkedServiceName, nameof(linkedServiceName));

            DatasetType = "HttpFile";
        }

        /// <summary> Initializes a new instance of DataFactoryHttpDataset. </summary>
        /// <param name="datasetType"> Type of dataset. </param>
        /// <param name="description"> Dataset description. </param>
        /// <param name="structure"> Columns that define the structure of the dataset. Type: array (or Expression with resultType array), itemType: DatasetDataElement. </param>
        /// <param name="schema"> Columns that define the physical type schema of the dataset. Type: array (or Expression with resultType array), itemType: DatasetSchemaDataElement. </param>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <param name="parameters"> Parameters for dataset. </param>
        /// <param name="annotations"> List of tags that can be used for describing the Dataset. </param>
        /// <param name="folder"> The folder that this Dataset is in. If not specified, Dataset will appear at the root level. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="relativeUri"> The relative URL based on the URL in the HttpLinkedService refers to an HTTP file Type: string (or Expression with resultType string). </param>
        /// <param name="requestMethod"> The HTTP method for the HTTP request. Type: string (or Expression with resultType string). </param>
        /// <param name="requestBody"> The body for the HTTP request. Type: string (or Expression with resultType string). </param>
        /// <param name="additionalHeaders">
        /// The headers for the HTTP Request. e.g. request-header-name-1:request-header-value-1
        /// ...
        /// request-header-name-n:request-header-value-n Type: string (or Expression with resultType string).
        /// </param>
        /// <param name="format">
        /// The format of files.
        /// Please note <see cref="DatasetStorageFormat"/> is the base class. According to the scenario, a derived class of the base class might need to be assigned here, or this property needs to be casted to one of the possible derived classes.
        /// The available derived classes include <see cref="DatasetAvroFormat"/>, <see cref="DatasetJsonFormat"/>, <see cref="DatasetOrcFormat"/>, <see cref="DatasetParquetFormat"/> and <see cref="DatasetTextFormat"/>.
        /// </param>
        /// <param name="compression"> The data compression method used on files. </param>
        internal DataFactoryHttpDataset(string datasetType, string description, DataFactoryElement<IList<DatasetDataElement>> structure, DataFactoryElement<IList<DatasetSchemaDataElement>> schema, DataFactoryLinkedServiceReference linkedServiceName, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, DatasetFolder folder, IDictionary<string, DataFactoryElement<string>> additionalProperties, DataFactoryElement<string> relativeUri, DataFactoryElement<string> requestMethod, DataFactoryElement<string> requestBody, DataFactoryElement<string> additionalHeaders, DatasetStorageFormat format, DatasetCompression compression) : base(datasetType, description, structure, schema, linkedServiceName, parameters, annotations, folder, additionalProperties)
        {
            RelativeUri = relativeUri;
            RequestMethod = requestMethod;
            RequestBody = requestBody;
            AdditionalHeaders = additionalHeaders;
            Format = format;
            Compression = compression;
            DatasetType = datasetType ?? "HttpFile";
        }

        /// <summary> The relative URL based on the URL in the HttpLinkedService refers to an HTTP file Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> RelativeUri { get; set; }
        /// <summary> The HTTP method for the HTTP request. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> RequestMethod { get; set; }
        /// <summary> The body for the HTTP request. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> RequestBody { get; set; }
        /// <summary>
        /// The headers for the HTTP Request. e.g. request-header-name-1:request-header-value-1
        /// ...
        /// request-header-name-n:request-header-value-n Type: string (or Expression with resultType string).
        /// </summary>
        public DataFactoryElement<string> AdditionalHeaders { get; set; }
        /// <summary>
        /// The format of files.
        /// Please note <see cref="DatasetStorageFormat"/> is the base class. According to the scenario, a derived class of the base class might need to be assigned here, or this property needs to be casted to one of the possible derived classes.
        /// The available derived classes include <see cref="DatasetAvroFormat"/>, <see cref="DatasetJsonFormat"/>, <see cref="DatasetOrcFormat"/>, <see cref="DatasetParquetFormat"/> and <see cref="DatasetTextFormat"/>.
        /// </summary>
        public DatasetStorageFormat Format { get; set; }
        /// <summary> The data compression method used on files. </summary>
        public DatasetCompression Compression { get; set; }
    }
}
