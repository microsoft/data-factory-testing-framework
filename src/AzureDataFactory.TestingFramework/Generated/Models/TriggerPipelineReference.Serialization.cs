// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class TriggerPipelineReference : IUtf8JsonSerializable
    {
        void IUtf8JsonSerializable.Write(Utf8JsonWriter writer)
        {
            writer.WriteStartObject();
            if (Optional.IsDefined(PipelineReference))
            {
                writer.WritePropertyName("pipelineReference"u8);
                writer.WriteObjectValue(PipelineReference);
            }
            if (Optional.IsCollectionDefined(Parameters))
            {
                writer.WritePropertyName("parameters"u8);
                writer.WriteStartObject();
                foreach (var item in Parameters)
                {
                    writer.WritePropertyName(item.Key);
                    if (item.Value == null)
                    {
                        writer.WriteNullValue();
                        continue;
                    }
#if NET6_0_OR_GREATER
				writer.WriteRawValue(item.Value);
#else
                    JsonSerializer.Serialize(writer, JsonDocument.Parse(item.Value.ToString()).RootElement);
#endif
                }
                writer.WriteEndObject();
            }
            writer.WriteEndObject();
        }

        internal static TriggerPipelineReference DeserializeTriggerPipelineReference(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            Optional<DataFactoryPipelineReference> pipelineReference = default;
            Optional<IDictionary<string, DataFactoryElement<string>>> parameters = default;
            foreach (var property in element.EnumerateObject())
            {
                if (property.NameEquals("pipelineReference"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    pipelineReference = DataFactoryPipelineReference.DeserializeDataFactoryPipelineReference(property.Value);
                    continue;
                }
                if (property.NameEquals("parameters"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    Dictionary<string, DataFactoryElement<string>> dictionary = new Dictionary<string, DataFactoryElement<string>>();
                    foreach (var property0 in property.Value.EnumerateObject())
                    {
                        if (property0.Value.ValueKind == JsonValueKind.Null)
                        {
                            dictionary.Add(property0.Name, null);
                        }
                        else
                        {
                            dictionary.Add(property0.Name, JsonSerializer.Deserialize<DataFactoryElement<string>>(property0.Value.GetRawText()));
                        }
                    }
                    parameters = dictionary;
                    continue;
                }
            }
            return new TriggerPipelineReference(pipelineReference.Value, Optional.ToDictionary(parameters));
        }
    }
}
