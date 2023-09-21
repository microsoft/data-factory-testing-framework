// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Properties of integration runtime node. </summary>
    public partial class ManagedIntegrationRuntimeNode
    {
        /// <summary> Initializes a new instance of ManagedIntegrationRuntimeNode. </summary>
        internal ManagedIntegrationRuntimeNode()
        {
            Errors = new ChangeTrackingList<ManagedIntegrationRuntimeError>();
            AdditionalProperties = new ChangeTrackingDictionary<string, DataFactoryElement<string>>();
        }

        /// <summary> Initializes a new instance of ManagedIntegrationRuntimeNode. </summary>
        /// <param name="nodeId"> The managed integration runtime node id. </param>
        /// <param name="status"> The managed integration runtime node status. </param>
        /// <param name="errors"> The errors that occurred on this integration runtime node. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        internal ManagedIntegrationRuntimeNode(string nodeId, ManagedIntegrationRuntimeNodeStatus? status, IReadOnlyList<ManagedIntegrationRuntimeError> errors, IReadOnlyDictionary<string, DataFactoryElement<string>> additionalProperties)
        {
            NodeId = nodeId;
            Status = status;
            Errors = errors;
            AdditionalProperties = additionalProperties;
        }

        /// <summary> The managed integration runtime node id. </summary>
        public string NodeId { get; }
        /// <summary> The managed integration runtime node status. </summary>
        public ManagedIntegrationRuntimeNodeStatus? Status { get; }
        /// <summary> The errors that occurred on this integration runtime node. </summary>
        public IReadOnlyList<ManagedIntegrationRuntimeError> Errors { get; }
        /// <summary>
        /// Additional Properties
        /// <para>
        /// To assign an object to the value of this property use <see cref="BinaryData.FromObjectAsJson{T}(T, System.Text.Json.JsonSerializerOptions?)"/>.
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
        public IReadOnlyDictionary<string, DataFactoryElement<string>> AdditionalProperties { get; }
    }
}
