// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Dynamics CRM linked service. </summary>
    public partial class DynamicsCrmLinkedService : DataFactoryLinkedServiceProperties
    {
        /// <summary> Initializes a new instance of DynamicsCrmLinkedService. </summary>
        /// <param name="deploymentType"> The deployment type of the Dynamics CRM instance. 'Online' for Dynamics CRM Online and 'OnPremisesWithIfd' for Dynamics CRM on-premises with Ifd. Type: string (or Expression with resultType string). </param>
        /// <param name="authenticationType"> The authentication type to connect to Dynamics CRM server. 'Office365' for online scenario, 'Ifd' for on-premises with Ifd scenario, 'AADServicePrincipal' for Server-To-Server authentication in online scenario. Type: string (or Expression with resultType string). </param>
        /// <exception cref="ArgumentNullException"> <paramref name="deploymentType"/> or <paramref name="authenticationType"/> is null. </exception>
        public DynamicsCrmLinkedService(DataFactoryElement<string> deploymentType, DataFactoryElement<string> authenticationType)
        {
            Argument.AssertNotNull(deploymentType, nameof(deploymentType));
            Argument.AssertNotNull(authenticationType, nameof(authenticationType));

            DeploymentType = deploymentType;
            AuthenticationType = authenticationType;
            LinkedServiceType = "DynamicsCrm";
        }

        /// <summary> Initializes a new instance of DynamicsCrmLinkedService. </summary>
        /// <param name="linkedServiceType"> Type of linked service. </param>
        /// <param name="connectVia"> The integration runtime reference. </param>
        /// <param name="description"> Linked service description. </param>
        /// <param name="parameters"> Parameters for linked service. </param>
        /// <param name="annotations"> List of tags that can be used for describing the linked service. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="deploymentType"> The deployment type of the Dynamics CRM instance. 'Online' for Dynamics CRM Online and 'OnPremisesWithIfd' for Dynamics CRM on-premises with Ifd. Type: string (or Expression with resultType string). </param>
        /// <param name="hostName"> The host name of the on-premises Dynamics CRM server. The property is required for on-prem and not allowed for online. Type: string (or Expression with resultType string). </param>
        /// <param name="port"> The port of on-premises Dynamics CRM server. The property is required for on-prem and not allowed for online. Default is 443. Type: integer (or Expression with resultType integer), minimum: 0. </param>
        /// <param name="serviceUri"> The URL to the Microsoft Dynamics CRM server. The property is required for on-line and not allowed for on-prem. Type: string (or Expression with resultType string). </param>
        /// <param name="organizationName"> The organization name of the Dynamics CRM instance. The property is required for on-prem and required for online when there are more than one Dynamics CRM instances associated with the user. Type: string (or Expression with resultType string). </param>
        /// <param name="authenticationType"> The authentication type to connect to Dynamics CRM server. 'Office365' for online scenario, 'Ifd' for on-premises with Ifd scenario, 'AADServicePrincipal' for Server-To-Server authentication in online scenario. Type: string (or Expression with resultType string). </param>
        /// <param name="username"> User name to access the Dynamics CRM instance. Type: string (or Expression with resultType string). </param>
        /// <param name="password"> Password to access the Dynamics CRM instance. </param>
        /// <param name="servicePrincipalId"> The client ID of the application in Azure Active Directory used for Server-To-Server authentication. Type: string (or Expression with resultType string). </param>
        /// <param name="servicePrincipalCredentialType"> The service principal credential type to use in Server-To-Server authentication. 'ServicePrincipalKey' for key/secret, 'ServicePrincipalCert' for certificate. Type: string (or Expression with resultType string). </param>
        /// <param name="servicePrincipalCredential"> The credential of the service principal object in Azure Active Directory. If servicePrincipalCredentialType is 'ServicePrincipalKey', servicePrincipalCredential can be SecureString or AzureKeyVaultSecretReference. If servicePrincipalCredentialType is 'ServicePrincipalCert', servicePrincipalCredential can only be AzureKeyVaultSecretReference. </param>
        /// <param name="encryptedCredential"> The encrypted credential used for authentication. Credentials are encrypted using the integration runtime credential manager. Type: string. </param>
        internal DynamicsCrmLinkedService(string linkedServiceType, IntegrationRuntimeReference connectVia, string description, IDictionary<string, EntityParameterSpecification> parameters, IList<BinaryData> annotations, IDictionary<string, DataFactoryElement<string>> additionalProperties, DataFactoryElement<string> deploymentType, DataFactoryElement<string> hostName, DataFactoryElement<int> port, DataFactoryElement<string> serviceUri, DataFactoryElement<string> organizationName, DataFactoryElement<string> authenticationType, DataFactoryElement<string> username, DataFactorySecretBaseDefinition password, DataFactoryElement<string> servicePrincipalId, DataFactoryElement<string> servicePrincipalCredentialType, DataFactorySecretBaseDefinition servicePrincipalCredential, string encryptedCredential) : base(linkedServiceType, connectVia, description, parameters, annotations, additionalProperties)
        {
            DeploymentType = deploymentType;
            HostName = hostName;
            Port = port;
            ServiceUri = serviceUri;
            OrganizationName = organizationName;
            AuthenticationType = authenticationType;
            Username = username;
            Password = password;
            ServicePrincipalId = servicePrincipalId;
            ServicePrincipalCredentialType = servicePrincipalCredentialType;
            ServicePrincipalCredential = servicePrincipalCredential;
            EncryptedCredential = encryptedCredential;
            LinkedServiceType = linkedServiceType ?? "DynamicsCrm";
        }

        /// <summary> The deployment type of the Dynamics CRM instance. 'Online' for Dynamics CRM Online and 'OnPremisesWithIfd' for Dynamics CRM on-premises with Ifd. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> DeploymentType { get; set; }
        /// <summary> The host name of the on-premises Dynamics CRM server. The property is required for on-prem and not allowed for online. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> HostName { get; set; }
        /// <summary> The port of on-premises Dynamics CRM server. The property is required for on-prem and not allowed for online. Default is 443. Type: integer (or Expression with resultType integer), minimum: 0. </summary>
        public DataFactoryElement<int> Port { get; set; }
        /// <summary> The URL to the Microsoft Dynamics CRM server. The property is required for on-line and not allowed for on-prem. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ServiceUri { get; set; }
        /// <summary> The organization name of the Dynamics CRM instance. The property is required for on-prem and required for online when there are more than one Dynamics CRM instances associated with the user. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> OrganizationName { get; set; }
        /// <summary> The authentication type to connect to Dynamics CRM server. 'Office365' for online scenario, 'Ifd' for on-premises with Ifd scenario, 'AADServicePrincipal' for Server-To-Server authentication in online scenario. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> AuthenticationType { get; set; }
        /// <summary> User name to access the Dynamics CRM instance. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> Username { get; set; }
        /// <summary> Password to access the Dynamics CRM instance. </summary>
        public DataFactorySecretBaseDefinition Password { get; set; }
        /// <summary> The client ID of the application in Azure Active Directory used for Server-To-Server authentication. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ServicePrincipalId { get; set; }
        /// <summary> The service principal credential type to use in Server-To-Server authentication. 'ServicePrincipalKey' for key/secret, 'ServicePrincipalCert' for certificate. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> ServicePrincipalCredentialType { get; set; }
        /// <summary> The credential of the service principal object in Azure Active Directory. If servicePrincipalCredentialType is 'ServicePrincipalKey', servicePrincipalCredential can be SecureString or AzureKeyVaultSecretReference. If servicePrincipalCredentialType is 'ServicePrincipalCert', servicePrincipalCredential can only be AzureKeyVaultSecretReference. </summary>
        public DataFactorySecretBaseDefinition ServicePrincipalCredential { get; set; }
        /// <summary> The encrypted credential used for authentication. Credentials are encrypted using the integration runtime credential manager. Type: string. </summary>
        public string EncryptedCredential { get; set; }
    }
}
