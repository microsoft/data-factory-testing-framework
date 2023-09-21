// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class ScriptActivityParameter : IUtf8JsonSerializable
    {
        void IUtf8JsonSerializable.Write(Utf8JsonWriter writer)
        {
            writer.WriteStartObject();
            if (Optional.IsDefined(Name))
            {
                writer.WritePropertyName("name"u8);
                JsonSerializer.Serialize(writer, Name);
            }
            if (Optional.IsDefined(ParameterType))
            {
                writer.WritePropertyName("type"u8);
                writer.WriteStringValue(ParameterType.Value.ToString());
            }
            if (Optional.IsDefined(Value))
            {
                writer.WritePropertyName("value"u8);
                JsonSerializer.Serialize(writer, Value);
            }
            if (Optional.IsDefined(Direction))
            {
                writer.WritePropertyName("direction"u8);
                writer.WriteStringValue(Direction.Value.ToString());
            }
            if (Optional.IsDefined(Size))
            {
                writer.WritePropertyName("size"u8);
                writer.WriteNumberValue(Size.Value);
            }
            writer.WriteEndObject();
        }

        internal static ScriptActivityParameter DeserializeScriptActivityParameter(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            Optional<DataFactoryElement<string>> name = default;
            Optional<ScriptActivityParameterType> type = default;
            Optional<DataFactoryElement<string>> value = default;
            Optional<ScriptActivityParameterDirection> direction = default;
            Optional<int> size = default;
            foreach (var property in element.EnumerateObject())
            {
                if (property.NameEquals("name"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    name = JsonSerializer.Deserialize<DataFactoryElement<string>>(property.Value.GetRawText());
                    continue;
                }
                if (property.NameEquals("type"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    type = new ScriptActivityParameterType(property.Value.GetString());
                    continue;
                }
                if (property.NameEquals("value"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    value = JsonSerializer.Deserialize<DataFactoryElement<string>>(property.Value.GetRawText());
                    continue;
                }
                if (property.NameEquals("direction"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    direction = new ScriptActivityParameterDirection(property.Value.GetString());
                    continue;
                }
                if (property.NameEquals("size"u8))
                {
                    if (property.Value.ValueKind == JsonValueKind.Null)
                    {
                        continue;
                    }
                    size = property.Value.GetInt32();
                    continue;
                }
            }
            return new ScriptActivityParameter(name.Value, Optional.ToNullable(type), value.Value, Optional.ToNullable(direction), Optional.ToNullable(size));
        }
    }
}
