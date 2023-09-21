// <auto-generated/>

#nullable disable

using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Linked service for Google Cloud Storage. </summary>
    public partial class GoogleCloudStorageLinkedService : DataFactoryLinkedServiceProperties
    {
        /// <summary> Initializes a new instance of GoogleCloudStorageLinkedService. </summary>
        public GoogleCloudStorageLinkedService()
        {
            LinkedServiceType = "GoogleCloudStorage";
        }

        /// <summary> Initializes a new instance of GoogleCloudStorageLinkedService. </summary>
        /// <param name="linkedServiceType"> Type of linked service. </param>
        /// <param name="connectVia"> The integration runtime reference. </param>
        /// <param name="description"> Linked service description. </param>
        /// <param name="parameters"> Parameters for linked service. </param>
        /// <param name="annotations"> List of tags that can be used for describing the linked service. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="accessKeyId"> The access key identifier of the Google Cloud Storage Identity and Access Management (IAM) user. Type: string (or Expression with resultType string). </param>
        /// <param name="secretAccessKey"> The secret access key of the Google Cloud Storage Identity and Access Management (IAM) user. </param>
        /// <param name="serviceUri"> This value specifies the endpoint to access with the Google Cloud Storage Connector. This is an optional property; change it only if you want to try a different service endpoint or want to switch between https and http. Type: string (or Expression with resultType string). </param>
        /// <param name="encryptedCredential"> The encrypted credential used for authentication. Credentials are encrypted using the integration runtime credential manager. Type: string. </param>
        internal GoogleCloudStorageLinkedService(string linkedServiceType, IntegrationRuntimeReference connectVia, string description, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, IDictionary<string, DataFactoryElement<string>> additionalProperties, DataFactoryElement<string> accessKeyId, DataFactorySecretBaseDefinition secretAccessKey, DataFactoryElement<string> serviceUri, string encryptedCredential) : base(linkedServiceType, connectVia, description, parameters, annotations, additionalProperties)
        {
            AccessKeyId = accessKeyId;
            SecretAccessKey = secretAccessKey;
            ServiceUri = serviceUri;
            EncryptedCredential = encryptedCredential;
            LinkedServiceType = linkedServiceType ?? "GoogleCloudStorage";
        }

        /// <summary> The access key identifier of the Google Cloud Storage Identity and Access Management (IAM) user. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> AccessKeyId { get; set; }
        /// <summary> The secret access key of the Google Cloud Storage Identity and Access Management (IAM) user. </summary>
        public DataFactorySecretBaseDefinition SecretAccessKey { get; set; }
        /// <summary> This value specifies the endpoint to access with the Google Cloud Storage Connector. This is an optional property; change it only if you want to try a different service endpoint or want to switch between https and http. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ServiceUri { get; set; }
        /// <summary> The encrypted credential used for authentication. Credentials are encrypted using the integration runtime credential manager. Type: string. </summary>
        public string EncryptedCredential { get; set; }
    }
}
