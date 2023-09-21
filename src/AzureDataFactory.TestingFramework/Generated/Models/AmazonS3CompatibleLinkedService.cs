// <auto-generated/>

#nullable disable

using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Linked service for Amazon S3 Compatible. </summary>
    public partial class AmazonS3CompatibleLinkedService : DataFactoryLinkedServiceProperties
    {
        /// <summary> Initializes a new instance of AmazonS3CompatibleLinkedService. </summary>
        public AmazonS3CompatibleLinkedService()
        {
            LinkedServiceType = "AmazonS3Compatible";
        }

        /// <summary> Initializes a new instance of AmazonS3CompatibleLinkedService. </summary>
        /// <param name="linkedServiceType"> Type of linked service. </param>
        /// <param name="connectVia"> The integration runtime reference. </param>
        /// <param name="description"> Linked service description. </param>
        /// <param name="parameters"> Parameters for linked service. </param>
        /// <param name="annotations"> List of tags that can be used for describing the linked service. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="accessKeyId"> The access key identifier of the Amazon S3 Compatible Identity and Access Management (IAM) user. Type: string (or Expression with resultType string). </param>
        /// <param name="secretAccessKey"> The secret access key of the Amazon S3 Compatible Identity and Access Management (IAM) user. </param>
        /// <param name="serviceUri"> This value specifies the endpoint to access with the Amazon S3 Compatible Connector. This is an optional property; change it only if you want to try a different service endpoint or want to switch between https and http. Type: string (or Expression with resultType string). </param>
        /// <param name="forcePathStyle"> If true, use S3 path-style access instead of virtual hosted-style access. Default value is false. Type: boolean (or Expression with resultType boolean). </param>
        /// <param name="encryptedCredential"> The encrypted credential used for authentication. Credentials are encrypted using the integration runtime credential manager. Type: string. </param>
        internal AmazonS3CompatibleLinkedService(string linkedServiceType, IntegrationRuntimeReference connectVia, string description, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, IDictionary<string, DataFactoryElement<string>> additionalProperties, DataFactoryElement<string> accessKeyId, DataFactorySecretBaseDefinition secretAccessKey, DataFactoryElement<string> serviceUri, DataFactoryElement<bool> forcePathStyle, string encryptedCredential) : base(linkedServiceType, connectVia, description, parameters, annotations, additionalProperties)
        {
            AccessKeyId = accessKeyId;
            SecretAccessKey = secretAccessKey;
            ServiceUri = serviceUri;
            ForcePathStyle = forcePathStyle;
            EncryptedCredential = encryptedCredential;
            LinkedServiceType = linkedServiceType ?? "AmazonS3Compatible";
        }

        /// <summary> The access key identifier of the Amazon S3 Compatible Identity and Access Management (IAM) user. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> AccessKeyId { get; set; }
        /// <summary> The secret access key of the Amazon S3 Compatible Identity and Access Management (IAM) user. </summary>
        public DataFactorySecretBaseDefinition SecretAccessKey { get; set; }
        /// <summary> This value specifies the endpoint to access with the Amazon S3 Compatible Connector. This is an optional property; change it only if you want to try a different service endpoint or want to switch between https and http. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ServiceUri { get; set; }
        /// <summary> If true, use S3 path-style access instead of virtual hosted-style access. Default value is false. Type: boolean (or Expression with resultType boolean). </summary>
        public DataFactoryElement<bool> ForcePathStyle { get; set; }
        /// <summary> The encrypted credential used for authentication. Credentials are encrypted using the integration runtime credential manager. Type: string. </summary>
        public string EncryptedCredential { get; set; }
    }
}
