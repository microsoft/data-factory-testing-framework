// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class FormatWriteSettings : IUtf8JsonSerializable
    {
        void IUtf8JsonSerializable.Write(Utf8JsonWriter writer)
        {
            writer.WriteStartObject();
            writer.WritePropertyName("type"u8);
            writer.WriteStringValue(FormatWriteSettingsType);
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

        internal static FormatWriteSettings DeserializeFormatWriteSettings(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            if (element.TryGetProperty("type", out JsonElement discriminator))
            {
                switch (discriminator.GetString())
                {
                    case "AvroWriteSettings": return AvroWriteSettings.DeserializeAvroWriteSettings(element);
                    case "JsonWriteSettings": return JsonWriteSettings.DeserializeJsonWriteSettings(element);
                    case "OrcWriteSettings": return OrcWriteSettings.DeserializeOrcWriteSettings(element);
                    case "ParquetWriteSettings": return ParquetWriteSettings.DeserializeParquetWriteSettings(element);
                    case "DelimitedTextWriteSettings": return DelimitedTextWriteSettings.DeserializeDelimitedTextWriteSettings(element);
                }
            }
            return UnknownFormatWriteSettings.DeserializeUnknownFormatWriteSettings(element);
        }
    }
}
