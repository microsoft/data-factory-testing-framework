// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;
using Azure.ResourceManager.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    internal partial class DataFactoryLinkedServiceListResult
    {
        internal static DataFactoryLinkedServiceListResult DeserializeDataFactoryLinkedServiceListResult(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            IReadOnlyList<DataFactoryLinkedServiceData> value = default;
            Optional<string> nextLink = default;
            foreach (var property in element.EnumerateObject())
            {
                if (property.NameEquals("value"u8))
                {
                    List<DataFactoryLinkedServiceData> array = new List<DataFactoryLinkedServiceData>();
                    foreach (var item in property.Value.EnumerateArray())
                    {
                        array.Add(DataFactoryLinkedServiceData.DeserializeDataFactoryLinkedServiceData(item));
                    }
                    value = array;
                    continue;
                }
                if (property.NameEquals("nextLink"u8))
                {
                    nextLink = property.Value.GetString();
                    continue;
                }
            }
            return new DataFactoryLinkedServiceListResult(value, nextLink.Value);
        }
    }
}
