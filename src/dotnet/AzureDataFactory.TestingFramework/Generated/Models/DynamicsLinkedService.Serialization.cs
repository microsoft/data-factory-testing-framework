// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class DynamicsLinkedService : IUtf8JsonSerializable
    {
        void IUtf8JsonSerializable.Write(Utf8JsonWriter writer)
        {
            writer.WriteStartObject();
            writer.WritePropertyName("type"u8);
            writer.WriteStringValue(LinkedServiceType);
            if (Optional.IsDefined(ConnectVia))
            {
                writer.WritePropertyName("connectVia"u8);
                writer.WriteObjectValue(ConnectVia);
            }
            if (Optional.IsDefined(Description))
            {
                writer.WritePropertyName("description"u8);
                writer.WriteStringValue(Description);
            }
            if (Optional.IsCollectionDefined(Parameters))
            {
                writer.WritePropertyName("parameters"u8);
                writer.WriteStartObject();
                foreach (var item in Parameters)
                {
                    writer.WritePropertyName(item.Key);
                    writer.WriteObjectValue(item.Value);
                }
                writer.WriteEndObject();
            }
            if (Optional.IsCollectionDefined(Annotations))
            {
                writer.WritePropertyName("annotations"u8);
                writer.WriteStartArray();
                foreach (var item in Annotations)
                {
                    if (item == null)
                    {
                        writer.WriteNullValue();
                        continue;
                    }
#if NET6_0_OR_GREATER
				writer.WriteRawValue(item);
#else
                    JsonSerializer.Serialize(writer, JsonDocument.Parse(item.ToString()).RootElement);
#endif
                }
                writer.WriteEndArray();
            }
            writer.WritePropertyName("typeProperties"u8);
            writer.WriteStartObject();
            writer.WritePropertyName("deploymentType"u8);
            JsonSerializer.Serialize(writer, DeploymentType);
            if (Optional.IsDefined(HostName))
            {
                writer.WritePropertyName("hostName"u8);
                JsonSerializer.Serialize(writer, HostName);
            }
            if (Optional.IsDefined(Port))
            {
                writer.WritePropertyName("port"u8);
                JsonSerializer.Serialize(writer, Port);
            }
            if (Optional.IsDefined(ServiceUri))
            {
                writer.WritePropertyName("serviceUri"u8);
                JsonSerializer.Serialize(writer, ServiceUri);
            }
            if (Optional.IsDefined(OrganizationName))
            {
                writer.WritePropertyName("organizationName"u8);
                JsonSerializer.Serialize(writer, OrganizationName);
            }
            writer.WritePropertyName("authenticationType"u8);
            JsonSerializer.Serialize(writer, AuthenticationType);
            if (Optional.IsDefined(Username))
            {
                writer.WritePropertyName("username"u8);
                JsonSerializer.Serialize(writer, Username);
            }
            if (Optional.IsDefined(Password))
            {
                writer.WritePropertyName("password"u8);
                JsonSerializer.Serialize(writer, Password);
            }
            if (Optional.IsDefined(ServicePrincipalId))
            {
                writer.WritePropertyName("servicePrincipalId"u8);
                JsonSerializer.Serialize(writer, ServicePrincipalId);
            }
            if (Optional.IsDefined(ServicePrincipalCredentialType))
            {
                writer.WritePropertyName("servicePrincipalCredentialType"u8);
                JsonSerializer.Serialize(writer, ServicePrincipalCredentialType);
            }
            if (Optional.IsDefined(ServicePrincipalCredential))
            {
                writer.WritePropertyName("servicePrincipalCredential"u8);
                JsonSerializer.Serialize(writer, ServicePrincipalCredential);
            }
            if (Optional.IsDefined(EncryptedCredential))
            {
                writer.WritePropertyName("encryptedCredential"u8);
                writer.WriteStringValue(EncryptedCredential);
            }
            if (Optional.IsDefined(Credential))
            {
                writer.WritePropertyName("credential"u8);
                writer.WriteObjectValue(Credential);
            }
            writer.WriteEndObject();
            foreach (var item in AdditionalProperties)
            {
                writer.WritePropertyName(item.Key);
#if NET6_0_OR_GREATER
				writer.WriteRawValue(item.Value);
#else
                JsonSerializer.Serialize(writer, JsonDocument.Parse(item.Value.ToString()).RootElement);
#endif
            }
            writer.WriteEndObject();
        }

        internal static DynamicsLinkedService DeserializeDynamicsLinkedService(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            string type = default;
            Optional<IntegrationRuntimeReference> connectVia = default;
            Optional<string> description = default;
            Optional<IDictionary<string, EntityParameterSpecification>> parameters = default;
            Optional<IList<BinaryData>> annotations = default;
            DataFactoryElement<string> deploymentType = default;
            Optional<DataFactoryElement<string>> hostName = default;
            Optional<DataFactoryElement<int>> port = default;
            Optional<DataFactoryElement<string>> serviceUri = default;
            Optional<DataFactoryElement<string>> organizationName = default;
            DataFactoryElement<string> authenticationType = default;
            Optional<DataFactoryElement<string>> username = default;
            Optional<DataFactorySecretBaseDefinition> password = default;
            Optional<DataFactoryElement<string>> servicePrincipalId = default;
            Optional<DataFactoryElement<string>> servicePrincipalCredentialType = default;
            Optional<DataFactorySecretBaseDefinition> servicePrincipalCredential = default;
            Optional<string> encryptedCredential = default;
            Optional<DataFactoryCredentialReference> credential = default;
            IDictionary<string, DataFactoryElement<string>> additionalProperties = default;
            Dictionary<string, DataFactoryElement<string>> additionalPropertiesDictionary = new Dictionary<string, DataFactoryElement<string>>();
            foreach (var property in element.EnumerateObject())
            {
                if (property.NameEquals("type"u8))
                {
                    type = property.Value.GetString();
                    continue;
                }
                if (property.NameEquals("connectVia"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    connectVia = IntegrationRuntimeReference.DeserializeIntegrationRuntimeReference(property.Value);
                    continue;
                }
                if (property.NameEquals("description"u8))
                {
                    description = property.Value.GetString();
                    continue;
                }
                if (property.NameEquals("parameters"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    Dictionary<string, EntityParameterSpecification> dictionary = new Dictionary<string, EntityParameterSpecification>();
                    foreach (var property0 in property.Value.EnumerateObject())
                    {
                        dictionary.Add(property0.Name, EntityParameterSpecification.DeserializeEntityParameterSpecification(property0.Value));
                    }
                    parameters = dictionary;
                    continue;
                }
                if (property.NameEquals("annotations"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    List<BinaryData> array = new List<BinaryData>();
                    foreach (var item in property.Value.EnumerateArray())
                    {
                        if (item.ValueKind == JsonValueKind.Null)
                        {
                            array.Add(null);
                        }
                        else
                        {
                            array.Add(BinaryData.FromString(item.GetRawText()));
                        }
                    }
                    annotations = array;
                    continue;
                }
                if (property.NameEquals("typeProperties"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        property.ThrowNonNullablePropertyIsNull();
                        continue;
                    }
                    foreach (var property0 in property.Value.EnumerateObject())
                    {
                        if (property0.NameEquals("deploymentType"u8))
                        {
                            deploymentType = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("hostName"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            hostName = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("port"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            port = JsonSerializer.Deserialize<DataFactoryElement<int>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("serviceUri"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            serviceUri = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("organizationName"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            organizationName = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("authenticationType"u8))
                        {
                            authenticationType = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("username"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            username = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("password"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            password = JsonSerializer.Deserialize<DataFactorySecretBaseDefinition>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("servicePrincipalId"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            servicePrincipalId = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("servicePrincipalCredentialType"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            servicePrincipalCredentialType = JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("servicePrincipalCredential"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            servicePrincipalCredential = JsonSerializer.Deserialize<DataFactorySecretBaseDefinition>(property0.Value.GetRawText());
                            continue;
                        }
                        if (property0.NameEquals("encryptedCredential"u8))
                        {
                            encryptedCredential = property0.Value.GetString();
                            continue;
                        }
                        if (property0.NameEquals("credential"u8))
                        {
                            if (property0.Value.ValueKind == JsonValueKind.Null)
                            {
                                continue;
                            }
                            credential = DataFactoryCredentialReference.DeserializeDataFactoryCredentialReference(property0.Value);
                            continue;
                        }
                    }
                    continue;
                }
                additionalPropertiesDictionary.Add(property.Name, JsonSerializer.Deserialize<DataFactoryElement<string>>(property.Value.GetRawText()));
            }
            additionalProperties = additionalPropertiesDictionary;
            return new DynamicsLinkedService(type, connectVia.Value, description.Value, Optional.ToDictionary(parameters), Optional.ToList(annotations), additionalProperties, deploymentType, hostName.Value, port.Value, serviceUri.Value, organizationName.Value, authenticationType, username.Value, password, servicePrincipalId.Value, servicePrincipalCredentialType.Value, servicePrincipalCredential, encryptedCredential.Value, credential.Value);
        }
    }
}