// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class DataFactoryDataFlowDebugSessionContent : IUtf8JsonSerializable
    {
        void IUtf8JsonSerializable.Write(Utf8JsonWriter writer)
        {
            writer.WriteStartObject();
            if (Optional.IsDefined(ComputeType))
            {
                writer.WritePropertyName("computeType"u8);
                writer.WriteStringValue(ComputeType);
            }
            if (Optional.IsDefined(CoreCount))
            {
                writer.WritePropertyName("coreCount"u8);
                writer.WriteNumberValue(CoreCount.Value);
            }
            if (Optional.IsDefined(TimeToLiveInMinutes))
            {
                writer.WritePropertyName("timeToLive"u8);
                writer.WriteNumberValue(TimeToLiveInMinutes.Value);
            }
            if (Optional.IsDefined(IntegrationRuntime))
            {
                writer.WritePropertyName("integrationRuntime"u8);
                writer.WriteObjectValue(IntegrationRuntime);
            }
            writer.WriteEndObject();
        }
    }
}
