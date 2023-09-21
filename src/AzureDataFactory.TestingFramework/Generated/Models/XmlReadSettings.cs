// <auto-generated/>

#nullable disable

using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Xml read settings. </summary>
    public partial class XmlReadSettings : FormatReadSettings
    {
        /// <summary> Initializes a new instance of XmlReadSettings. </summary>
        public XmlReadSettings()
        {
            FormatReadSettingsType = "XmlReadSettings";
        }

        /// <summary> Initializes a new instance of XmlReadSettings. </summary>
        /// <param name="formatReadSettingsType"> The read setting type. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="compressionProperties">
        /// Compression settings.
        /// Please note <see cref="CompressionReadSettings"/> is the base class. According to the scenario, a derived class of the base class might need to be assigned here, or this property needs to be casted to one of the possible derived classes.
        /// The available derived classes include <see cref="TarGzipReadSettings"/>, <see cref="TarReadSettings"/> and <see cref="ZipDeflateReadSettings"/>.
        /// </param>
        /// <param name="validationMode"> Indicates what validation method is used when reading the xml files. Allowed values: 'none', 'xsd', or 'dtd'. Type: string (or Expression with resultType string). </param>
        /// <param name="detectDataType"> Indicates whether type detection is enabled when reading the xml files. Type: boolean (or Expression with resultType boolean). </param>
        /// <param name="namespaces"> Indicates whether namespace is enabled when reading the xml files. Type: boolean (or Expression with resultType boolean). </param>
        /// <param name="namespacePrefixes"> Namespace uri to prefix mappings to override the prefixes in column names when namespace is enabled, if no prefix is defined for a namespace uri, the prefix of xml element/attribute name in the xml data file will be used. Example: "{"http://www.example.com/xml":"prefix"}" Type: object (or Expression with resultType object). </param>
        internal XmlReadSettings(string formatReadSettingsType, IDictionary<string, DataFactoryElement<string>> additionalProperties, CompressionReadSettings compressionProperties, DataFactoryElement<string> validationMode, DataFactoryElement<bool> detectDataType, DataFactoryElement<bool> namespaces, BinaryData namespacePrefixes) : base(formatReadSettingsType, additionalProperties)
        {
            CompressionProperties = compressionProperties;
            ValidationMode = validationMode;
            DetectDataType = detectDataType;
            Namespaces = namespaces;
            NamespacePrefixes = namespacePrefixes;
            FormatReadSettingsType = formatReadSettingsType ?? "XmlReadSettings";
        }

        /// <summary>
        /// Compression settings.
        /// Please note <see cref="CompressionReadSettings"/> is the base class. According to the scenario, a derived class of the base class might need to be assigned here, or this property needs to be casted to one of the possible derived classes.
        /// The available derived classes include <see cref="TarGzipReadSettings"/>, <see cref="TarReadSettings"/> and <see cref="ZipDeflateReadSettings"/>.
        /// </summary>
        public CompressionReadSettings CompressionProperties { get; set; }
        /// <summary> Indicates what validation method is used when reading the xml files. Allowed values: 'none', 'xsd', or 'dtd'. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ValidationMode { get; set; }
        /// <summary> Indicates whether type detection is enabled when reading the xml files. Type: boolean (or Expression with resultType boolean). </summary>
        public DataFactoryElement<bool> DetectDataType { get; set; }
        /// <summary> Indicates whether namespace is enabled when reading the xml files. Type: boolean (or Expression with resultType boolean). </summary>
        public DataFactoryElement<bool> Namespaces { get; set; }
        /// <summary>
        /// Namespace uri to prefix mappings to override the prefixes in column names when namespace is enabled, if no prefix is defined for a namespace uri, the prefix of xml element/attribute name in the xml data file will be used. Example: "{"http://www.example.com/xml":"prefix"}" Type: object (or Expression with resultType object).
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
        public BinaryData NamespacePrefixes { get; set; }
    }
}
