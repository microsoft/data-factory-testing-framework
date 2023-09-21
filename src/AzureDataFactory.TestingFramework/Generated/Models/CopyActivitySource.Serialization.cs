// <auto-generated/>

#nullable disable

using System.Text.Json;
using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    public partial class CopyActivitySource : IUtf8JsonSerializable
    {
        void IUtf8JsonSerializable.Write(Utf8JsonWriter writer)
        {
            writer.WriteStartObject();
            writer.WritePropertyName("type"u8);
            writer.WriteStringValue(CopySourceType);
            if (Optional.IsDefined(SourceRetryCount))
            {
                writer.WritePropertyName("sourceRetryCount"u8);
                JsonSerializer.Serialize(writer, SourceRetryCount);
            }
            if (Optional.IsDefined(SourceRetryWait))
            {
                writer.WritePropertyName("sourceRetryWait"u8);
                JsonSerializer.Serialize(writer, SourceRetryWait);
            }
            if (Optional.IsDefined(MaxConcurrentConnections))
            {
                writer.WritePropertyName("maxConcurrentConnections"u8);
                JsonSerializer.Serialize(writer, MaxConcurrentConnections);
            }
            if (Optional.IsDefined(DisableMetricsCollection))
            {
                writer.WritePropertyName("disableMetricsCollection"u8);
                JsonSerializer.Serialize(writer, DisableMetricsCollection);
            }
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

        internal static CopyActivitySource DeserializeCopyActivitySource(JsonElement element)
        {
            if (element.ValueKind == JsonValueKind.Null)
            {
                return null;
            }
            if (element.TryGetProperty("type", out JsonElement discriminator))
            {
                switch (discriminator.GetString())
                {
                    case "AmazonMWSSource": return AmazonMwsSource.DeserializeAmazonMwsSource(element);
                    case "AmazonRdsForOracleSource": return AmazonRdsForOracleSource.DeserializeAmazonRdsForOracleSource(element);
                    case "AmazonRdsForSqlServerSource": return AmazonRdsForSqlServerSource.DeserializeAmazonRdsForSqlServerSource(element);
                    case "AmazonRedshiftSource": return AmazonRedshiftSource.DeserializeAmazonRedshiftSource(element);
                    case "AvroSource": return AvroSource.DeserializeAvroSource(element);
                    case "AzureBlobFSSource": return AzureBlobFSSource.DeserializeAzureBlobFSSource(element);
                    case "AzureDataExplorerSource": return AzureDataExplorerSource.DeserializeAzureDataExplorerSource(element);
                    case "AzureDataLakeStoreSource": return AzureDataLakeStoreSource.DeserializeAzureDataLakeStoreSource(element);
                    case "AzureDatabricksDeltaLakeSource": return AzureDatabricksDeltaLakeSource.DeserializeAzureDatabricksDeltaLakeSource(element);
                    case "AzureMariaDBSource": return AzureMariaDBSource.DeserializeAzureMariaDBSource(element);
                    case "AzureMySqlSource": return AzureMySqlSource.DeserializeAzureMySqlSource(element);
                    case "AzurePostgreSqlSource": return AzurePostgreSqlSource.DeserializeAzurePostgreSqlSource(element);
                    case "AzureSqlSource": return AzureSqlSource.DeserializeAzureSqlSource(element);
                    case "AzureTableSource": return AzureTableSource.DeserializeAzureTableSource(element);
                    case "BinarySource": return BinarySource.DeserializeBinarySource(element);
                    case "BlobSource": return DataFactoryBlobSource.DeserializeDataFactoryBlobSource(element);
                    case "CassandraSource": return CassandraSource.DeserializeCassandraSource(element);
                    case "CommonDataServiceForAppsSource": return CommonDataServiceForAppsSource.DeserializeCommonDataServiceForAppsSource(element);
                    case "ConcurSource": return ConcurSource.DeserializeConcurSource(element);
                    case "CosmosDbMongoDbApiSource": return CosmosDBMongoDBApiSource.DeserializeCosmosDBMongoDBApiSource(element);
                    case "CosmosDbSqlApiSource": return CosmosDBSqlApiSource.DeserializeCosmosDBSqlApiSource(element);
                    case "CouchbaseSource": return CouchbaseSource.DeserializeCouchbaseSource(element);
                    case "Db2Source": return Db2Source.DeserializeDb2Source(element);
                    case "DelimitedTextSource": return DelimitedTextSource.DeserializeDelimitedTextSource(element);
                    case "DocumentDbCollectionSource": return DocumentDBCollectionSource.DeserializeDocumentDBCollectionSource(element);
                    case "DrillSource": return DrillSource.DeserializeDrillSource(element);
                    case "DynamicsAXSource": return DynamicsAXSource.DeserializeDynamicsAXSource(element);
                    case "DynamicsCrmSource": return DynamicsCrmSource.DeserializeDynamicsCrmSource(element);
                    case "DynamicsSource": return DynamicsSource.DeserializeDynamicsSource(element);
                    case "EloquaSource": return EloquaSource.DeserializeEloquaSource(element);
                    case "ExcelSource": return ExcelSource.DeserializeExcelSource(element);
                    case "FileSystemSource": return FileSystemSource.DeserializeFileSystemSource(element);
                    case "GoogleAdWordsSource": return GoogleAdWordsSource.DeserializeGoogleAdWordsSource(element);
                    case "GoogleBigQuerySource": return GoogleBigQuerySource.DeserializeGoogleBigQuerySource(element);
                    case "GreenplumSource": return GreenplumSource.DeserializeGreenplumSource(element);
                    case "HBaseSource": return HBaseSource.DeserializeHBaseSource(element);
                    case "HdfsSource": return HdfsSource.DeserializeHdfsSource(element);
                    case "HiveSource": return HiveSource.DeserializeHiveSource(element);
                    case "HttpSource": return DataFactoryHttpFileSource.DeserializeDataFactoryHttpFileSource(element);
                    case "HubspotSource": return HubspotSource.DeserializeHubspotSource(element);
                    case "ImpalaSource": return ImpalaSource.DeserializeImpalaSource(element);
                    case "InformixSource": return InformixSource.DeserializeInformixSource(element);
                    case "JiraSource": return JiraSource.DeserializeJiraSource(element);
                    case "JsonSource": return JsonSource.DeserializeJsonSource(element);
                    case "MagentoSource": return MagentoSource.DeserializeMagentoSource(element);
                    case "MariaDBSource": return MariaDBSource.DeserializeMariaDBSource(element);
                    case "MarketoSource": return MarketoSource.DeserializeMarketoSource(element);
                    case "MicrosoftAccessSource": return MicrosoftAccessSource.DeserializeMicrosoftAccessSource(element);
                    case "MongoDbAtlasSource": return MongoDBAtlasSource.DeserializeMongoDBAtlasSource(element);
                    case "MongoDbSource": return MongoDBSource.DeserializeMongoDBSource(element);
                    case "MongoDbV2Source": return MongoDBV2Source.DeserializeMongoDBV2Source(element);
                    case "MySqlSource": return MySqlSource.DeserializeMySqlSource(element);
                    case "NetezzaSource": return NetezzaSource.DeserializeNetezzaSource(element);
                    case "ODataSource": return ODataSource.DeserializeODataSource(element);
                    case "OdbcSource": return OdbcSource.DeserializeOdbcSource(element);
                    case "Office365Source": return Office365Source.DeserializeOffice365Source(element);
                    case "OracleServiceCloudSource": return OracleServiceCloudSource.DeserializeOracleServiceCloudSource(element);
                    case "OracleSource": return OracleSource.DeserializeOracleSource(element);
                    case "OrcSource": return OrcSource.DeserializeOrcSource(element);
                    case "ParquetSource": return ParquetSource.DeserializeParquetSource(element);
                    case "PaypalSource": return PaypalSource.DeserializePaypalSource(element);
                    case "PhoenixSource": return PhoenixSource.DeserializePhoenixSource(element);
                    case "PostgreSqlSource": return PostgreSqlSource.DeserializePostgreSqlSource(element);
                    case "PrestoSource": return PrestoSource.DeserializePrestoSource(element);
                    case "QuickBooksSource": return QuickBooksSource.DeserializeQuickBooksSource(element);
                    case "RelationalSource": return RelationalSource.DeserializeRelationalSource(element);
                    case "ResponsysSource": return ResponsysSource.DeserializeResponsysSource(element);
                    case "RestSource": return RestSource.DeserializeRestSource(element);
                    case "SalesforceMarketingCloudSource": return SalesforceMarketingCloudSource.DeserializeSalesforceMarketingCloudSource(element);
                    case "SalesforceServiceCloudSource": return SalesforceServiceCloudSource.DeserializeSalesforceServiceCloudSource(element);
                    case "SalesforceSource": return SalesforceSource.DeserializeSalesforceSource(element);
                    case "SapBwSource": return SapBWSource.DeserializeSapBWSource(element);
                    case "SapCloudForCustomerSource": return SapCloudForCustomerSource.DeserializeSapCloudForCustomerSource(element);
                    case "SapEccSource": return SapEccSource.DeserializeSapEccSource(element);
                    case "SapHanaSource": return SapHanaSource.DeserializeSapHanaSource(element);
                    case "SapOdpSource": return SapOdpSource.DeserializeSapOdpSource(element);
                    case "SapOpenHubSource": return SapOpenHubSource.DeserializeSapOpenHubSource(element);
                    case "SapTableSource": return SapTableSource.DeserializeSapTableSource(element);
                    case "ServiceNowSource": return ServiceNowSource.DeserializeServiceNowSource(element);
                    case "SharePointOnlineListSource": return SharePointOnlineListSource.DeserializeSharePointOnlineListSource(element);
                    case "ShopifySource": return ShopifySource.DeserializeShopifySource(element);
                    case "SnowflakeSource": return SnowflakeSource.DeserializeSnowflakeSource(element);
                    case "SparkSource": return SparkSource.DeserializeSparkSource(element);
                    case "SqlDWSource": return SqlDWSource.DeserializeSqlDWSource(element);
                    case "SqlMISource": return SqlMISource.DeserializeSqlMISource(element);
                    case "SqlServerSource": return SqlServerSource.DeserializeSqlServerSource(element);
                    case "SqlSource": return SqlSource.DeserializeSqlSource(element);
                    case "SquareSource": return SquareSource.DeserializeSquareSource(element);
                    case "SybaseSource": return SybaseSource.DeserializeSybaseSource(element);
                    case "TabularSource": return TabularSource.DeserializeTabularSource(element);
                    case "TeradataSource": return TeradataSource.DeserializeTeradataSource(element);
                    case "VerticaSource": return VerticaSource.DeserializeVerticaSource(element);
                    case "WebSource": return WebSource.DeserializeWebSource(element);
                    case "XeroSource": return XeroSource.DeserializeXeroSource(element);
                    case "XmlSource": return XmlSource.DeserializeXmlSource(element);
                    case "ZohoSource": return ZohoSource.DeserializeZohoSource(element);
                }
            }
            return UnknownCopySource.DeserializeUnknownCopySource(element);
        }
    }
}
