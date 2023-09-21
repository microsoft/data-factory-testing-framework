// <auto-generated/>

#nullable disable

using Azure.Core;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Data flow flowlet. </summary>
    public partial class DataFactoryFlowletProperties : DataFactoryDataFlowProperties
    {
        /// <summary> Initializes a new instance of DataFactoryFlowletProperties. </summary>
        public DataFactoryFlowletProperties()
        {
            Sources = new ChangeTrackingList<DataFlowSource>();
            Sinks = new ChangeTrackingList<DataFlowSink>();
            Transformations = new ChangeTrackingList<DataFlowTransformation>();
            ScriptLines = new ChangeTrackingList<string>();
            DataFlowType = "Flowlet";
        }

        /// <summary> Initializes a new instance of DataFactoryFlowletProperties. </summary>
        /// <param name="dataFlowType"> Type of data flow. </param>
        /// <param name="description"> The description of the data flow. </param>
        /// <param name="annotations"> List of tags that can be used for describing the data flow. </param>
        /// <param name="folder"> The folder that this data flow is in. If not specified, Data flow will appear at the root level. </param>
        /// <param name="sources"> List of sources in Flowlet. </param>
        /// <param name="sinks"> List of sinks in Flowlet. </param>
        /// <param name="transformations"> List of transformations in Flowlet. </param>
        /// <param name="script"> Flowlet script. </param>
        /// <param name="scriptLines"> Flowlet script lines. </param>
        internal DataFactoryFlowletProperties(string dataFlowType, string description, IList<BinaryData> annotations, DataFlowFolder folder, IList<DataFlowSource> sources, IList<DataFlowSink> sinks, IList<DataFlowTransformation> transformations, string script, IList<string> scriptLines) : base(dataFlowType, description, annotations, folder)
        {
            Sources = sources;
            Sinks = sinks;
            Transformations = transformations;
            Script = script;
            ScriptLines = scriptLines;
            DataFlowType = dataFlowType ?? "Flowlet";
        }

        /// <summary> List of sources in Flowlet. </summary>
        public IList<DataFlowSource> Sources { get; }
        /// <summary> List of sinks in Flowlet. </summary>
        public IList<DataFlowSink> Sinks { get; }
        /// <summary> List of transformations in Flowlet. </summary>
        public IList<DataFlowTransformation> Transformations { get; }
        /// <summary> Flowlet script. </summary>
        public string Script { get; set; }
        /// <summary> Flowlet script lines. </summary>
        public IList<string> ScriptLines { get; }
    }
}
