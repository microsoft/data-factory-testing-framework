// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class DataFactoryDataFlowDebugCommandResult
    {
        internal static DataFactoryDataFlowDebugCommandResult DeserializeDataFactoryDataFlowDebugCommandResult(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            Optional<string> status = default;
            Optional<string> data = default;
            foreach (var property in element.EnumerateObject())
            {
                if (property.NameEquals("status"u8))
                {
                    status = property.Value.GetString();
                    continue;
                }
                if (property.NameEquals("data"u8))
                {
                    data = property.Value.GetString();
                    continue;
                }
            }
            return new DataFactoryDataFlowDebugCommandResult(status.Value, data.Value);
        }
    }
}