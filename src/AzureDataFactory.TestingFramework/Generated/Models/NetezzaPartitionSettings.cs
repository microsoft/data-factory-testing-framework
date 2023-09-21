// <auto-generated/>

#nullable disable

using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> The settings that will be leveraged for Netezza source partitioning. </summary>
    public partial class NetezzaPartitionSettings
    {
        /// <summary> Initializes a new instance of NetezzaPartitionSettings. </summary>
        public NetezzaPartitionSettings()
        {
        }

        /// <summary> Initializes a new instance of NetezzaPartitionSettings. </summary>
        /// <param name="partitionColumnName"> The name of the column in integer type that will be used for proceeding range partitioning. Type: string (or Expression with resultType string). </param>
        /// <param name="partitionUpperBound"> The maximum value of column specified in partitionColumnName that will be used for proceeding range partitioning. Type: string (or Expression with resultType string). </param>
        /// <param name="partitionLowerBound"> The minimum value of column specified in partitionColumnName that will be used for proceeding range partitioning. Type: string (or Expression with resultType string). </param>
        internal NetezzaPartitionSettings(DataFactoryElement<string> partitionColumnName, DataFactoryElement<string> partitionUpperBound, DataFactoryElement<string> partitionLowerBound)
        {
            PartitionColumnName = partitionColumnName;
            PartitionUpperBound = partitionUpperBound;
            PartitionLowerBound = partitionLowerBound;
        }

        /// <summary> The name of the column in integer type that will be used for proceeding range partitioning. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> PartitionColumnName { get; set; }
        /// <summary> The maximum value of column specified in partitionColumnName that will be used for proceeding range partitioning. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> PartitionUpperBound { get; set; }
        /// <summary> The minimum value of column specified in partitionColumnName that will be used for proceeding range partitioning. Type: string (or Expression with resultType string). </summary>
        public DataFactoryElement<string> PartitionLowerBound { get; set; }
    }
}
