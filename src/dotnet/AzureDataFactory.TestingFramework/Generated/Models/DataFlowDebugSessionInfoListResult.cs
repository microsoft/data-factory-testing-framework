// <auto-generated/>

#nullable disable

using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> A list of active debug sessions. </summary>
    internal partial class DataFlowDebugSessionInfoListResult
    {
        /// <summary> Initializes a new instance of DataFlowDebugSessionInfoListResult. </summary>
        internal DataFlowDebugSessionInfoListResult()
        {
            Value = new ChangeTrackingList<DataFlowDebugSessionInfo>();
        }

        /// <summary> Initializes a new instance of DataFlowDebugSessionInfoListResult. </summary>
        /// <param name="value"> Array with all active debug sessions. </param>
        /// <param name="nextLink"> The link to the next page of results, if any remaining results exist. </param>
        internal DataFlowDebugSessionInfoListResult(IReadOnlyList<DataFlowDebugSessionInfo> value, string nextLink)
        {
            Value = value;
            NextLink = nextLink;
        }

        /// <summary> Array with all active debug sessions. </summary>
        public IReadOnlyList<DataFlowDebugSessionInfo> Value { get; }
        /// <summary> The link to the next page of results, if any remaining results exist. </summary>
        public string NextLink { get; }
    }
}