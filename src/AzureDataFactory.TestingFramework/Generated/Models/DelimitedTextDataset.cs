// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Delimited text dataset. </summary>
    public partial class DelimitedTextDataset : DataFactoryDatasetProperties
    {
        /// <summary> Initializes a new instance of DelimitedTextDataset. </summary>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="linkedServiceName"/> is null. </exception>
        public DelimitedTextDataset(DataFactoryLinkedServiceReference linkedServiceName) : base(linkedServiceName)
        {
            Argument.AssertNotNull(linkedServiceName, nameof(linkedServiceName));

            DatasetType = "DelimitedText";
        }

        /// <summary> Initializes a new instance of DelimitedTextDataset. </summary>
        /// <param name="datasetType"> Type of dataset. </param>
        /// <param name="description"> Dataset description. </param>
        /// <param name="structure"> Columns that define the structure of the dataset. Type: array (or Expression with resultType array), itemType: DatasetDataElement. </param>
        /// <param name="schema"> Columns that define the physical type schema of the dataset. Type: array (or Expression with resultType array), itemType: DatasetSchemaDataElement. </param>
        /// <param name="linkedServiceName"> Linked service reference. </param>
        /// <param name="parameters"> Parameters for dataset. </param>
        /// <param name="annotations"> List of tags that can be used for describing the Dataset. </param>
        /// <param name="folder"> The folder that this Dataset is in. If not specified, Dataset will appear at the root level. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="dataLocation">
        /// The location of the delimited text storage.
        /// Please note <see cref="DatasetLocation"/> is the base class. According to the scenario, a derived class of the base class might need to be assigned here, or this property needs to be casted to one of the possible derived classes.
        /// The available derived classes include <see cref="AmazonS3CompatibleLocation"/>, <see cref="AmazonS3Location"/>, <see cref="AzureBlobFSLocation"/>, <see cref="AzureBlobStorageLocation"/>, <see cref="AzureDataLakeStoreLocation"/>, <see cref="AzureFileStorageLocation"/>, <see cref="FileServerLocation"/>, <see cref="FtpServerLocation"/>, <see cref="GoogleCloudStorageLocation"/>, <see cref="HdfsLocation"/>, <see cref="HttpServerLocation"/>, <see cref="OracleCloudStorageLocation"/> and <see cref="SftpLocation"/>.
        /// </param>
        /// <param name="columnDelimiter"> The column delimiter. Type: string (or Expression with resultType string). </param>
        /// <param name="rowDelimiter"> The row delimiter. Type: string (or Expression with resultType string). </param>
        /// <param name="encodingName"> The code page name of the preferred encoding. If miss, the default value is UTF-8, unless BOM denotes another Unicode encoding. Refer to the name column of the table in the following link to set supported values: https://msdn.microsoft.com/library/system.text.encoding.aspx. Type: string (or Expression with resultType string). </param>
        /// <param name="compressionCodec"> The data compressionCodec. Type: string (or Expression with resultType string). </param>
        /// <param name="compressionLevel"> The data compression method used for DelimitedText. </param>
        /// <param name="quoteChar"> The quote character. Type: string (or Expression with resultType string). </param>
        /// <param name="escapeChar"> The escape character. Type: string (or Expression with resultType string). </param>
        /// <param name="firstRowAsHeader"> When used as input, treat the first row of data as headers. When used as output,write the headers into the output as the first row of data. The default value is false. Type: boolean (or Expression with resultType boolean). </param>
        /// <param name="nullValue"> The null value string. Type: string (or Expression with resultType string). </param>
        internal DelimitedTextDataset(string datasetType, string description, DataFactoryElement<IList<DatasetDataElement>> structure, DataFactoryElement<IList<DatasetSchemaDataElement>> schema, DataFactoryLinkedServiceReference linkedServiceName, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, DatasetFolder folder, IDictionary<string, DataFactoryElement<string>> additionalProperties, DatasetLocation dataLocation, DataFactoryElement<string> columnDelimiter, DataFactoryElement<string> rowDelimiter, DataFactoryElement<string> encodingName, DataFactoryElement<string> compressionCodec, BinaryData compressionLevel, DataFactoryElement<string> quoteChar, DataFactoryElement<string> escapeChar, DataFactoryElement<bool> firstRowAsHeader, DataFactoryElement<string> nullValue) : base(datasetType, description, structure, schema, linkedServiceName, parameters, annotations, folder, additionalProperties)
        {
            DataLocation = dataLocation;
            ColumnDelimiter = columnDelimiter;
            RowDelimiter = rowDelimiter;
            EncodingName = encodingName;
            CompressionCodec = compressionCodec;
            CompressionLevel = compressionLevel;
            QuoteChar = quoteChar;
            EscapeChar = escapeChar;
            FirstRowAsHeader = firstRowAsHeader;
            NullValue = nullValue;
            DatasetType = datasetType ?? "DelimitedText";
        }

        /// <summary>
        /// The location of the delimited text storage.
        /// Please note <see cref="DatasetLocation"/> is the base class. According to the scenario, a derived class of the base class might need to be assigned here, or this property needs to be casted to one of the possible derived classes.
        /// The available derived classes include <see cref="AmazonS3CompatibleLocation"/>, <see cref="AmazonS3Location"/>, <see cref="AzureBlobFSLocation"/>, <see cref="AzureBlobStorageLocation"/>, <see cref="AzureDataLakeStoreLocation"/>, <see cref="AzureFileStorageLocation"/>, <see cref="FileServerLocation"/>, <see cref="FtpServerLocation"/>, <see cref="GoogleCloudStorageLocation"/>, <see cref="HdfsLocation"/>, <see cref="HttpServerLocation"/>, <see cref="OracleCloudStorageLocation"/> and <see cref="SftpLocation"/>.
        /// </summary>
        public DatasetLocation DataLocation { get; set; }
        /// <summary> The column delimiter. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ColumnDelimiter { get; set; }
        /// <summary> The row delimiter. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> RowDelimiter { get; set; }
        /// <summary> The code page name of the preferred encoding. If miss, the default value is UTF-8, unless BOM denotes another Unicode encoding. Refer to the name column of the table in the following link to set supported values: https://msdn.microsoft.com/library/system.text.encoding.aspx. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> EncodingName { get; set; }
        /// <summary> The data compressionCodec. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> CompressionCodec { get; set; }
        /// <summary>
        /// The data compression method used for DelimitedText.
        /// <para>
        /// To assign an object to this property use <see cref="BinaryData.FromObjectAsJson{T}(T, System.Text.Json.JsonSerializerOptions?)"/>.
        /// </para>
        /// <para>
        /// To assign an already formated json string to this property use <see cref="BinaryData.FromString(string)"/>.
        /// </para>
        /// <para>
        /// Examples:
        /// <list type="bullet">
        /// <item>
        /// <term>BinaryData.FromObjectAsJson("foo")</term>
        /// <description>Creates a payload of "foo".</description>
        /// </item>
        /// <item>
        /// <term>BinaryData.FromString("\"foo\"")</term>
        /// <description>Creates a payload of "foo".</description>
        /// </item>
        /// <item>
        /// <term>BinaryData.FromObjectAsJson(new { key = "value" })</term>
        /// <description>Creates a payload of { "key": "value" }.</description>
        /// </item>
        /// <item>
        /// <term>BinaryData.FromString("{\"key\": \"value\"}")</term>
        /// <description>Creates a payload of { "key": "value" }.</description>
        /// </item>
        /// </list>
        /// </para>
        /// </summary>
        public BinaryData CompressionLevel { get; set; }
        /// <summary> The quote character. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> QuoteChar { get; set; }
        /// <summary> The escape character. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> EscapeChar { get; set; }
        /// <summary> When used as input, treat the first row of data as headers. When used as output,write the headers into the output as the first row of data. The default value is false. Type: boolean (or Expression with resultType boolean). </summary>
        public DataFactoryElement<bool> FirstRowAsHeader { get; set; }
        /// <summary> The null value string. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> NullValue { get; set; }
    }
}
