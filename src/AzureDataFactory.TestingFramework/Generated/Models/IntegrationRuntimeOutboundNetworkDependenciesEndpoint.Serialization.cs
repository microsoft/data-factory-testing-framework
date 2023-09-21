// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class IntegrationRuntimeOutboundNetworkDependenciesEndpoint
    {
        internal static IntegrationRuntimeOutboundNetworkDependenciesEndpoint DeserializeIntegrationRuntimeOutboundNetworkDependenciesEndpoint(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            Optional<string> domainName = default;
            Optional<IReadOnlyList<IntegrationRuntimeOutboundNetworkDependenciesEndpointDetails>> endpointDetails = default;
            foreach (var property in element.EnumerateObject())
            {
                if (property.NameEquals("domainName"u8))
                {
                    domainName = property.Value.GetString();
                    continue;
                }
                if (property.NameEquals("endpointDetails"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    List<IntegrationRuntimeOutboundNetworkDependenciesEndpointDetails> array = new List<IntegrationRuntimeOutboundNetworkDependenciesEndpointDetails>();
                    foreach (var item in property.Value.EnumerateArray())
                    {
                        array.Add(IntegrationRuntimeOutboundNetworkDependenciesEndpointDetails.DeserializeIntegrationRuntimeOutboundNetworkDependenciesEndpointDetails(item));
                    }
                    endpointDetails = array;
                    continue;
                }
            }
            return new IntegrationRuntimeOutboundNetworkDependenciesEndpoint(domainName.Value, Optional.ToList(endpointDetails));
        }
    }
}
