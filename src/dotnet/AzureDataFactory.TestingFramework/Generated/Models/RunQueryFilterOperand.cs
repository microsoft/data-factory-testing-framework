// <auto-generated/>

#nullable disable

using System.ComponentModel;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Parameter name to be used for filter. The allowed operands to query pipeline runs are PipelineName, RunStart, RunEnd and Status; to query activity runs are ActivityName, ActivityRunStart, ActivityRunEnd, ActivityType and Status, and to query trigger runs are TriggerName, TriggerRunTimestamp and Status. </summary>
    public readonly partial struct RunQueryFilterOperand : IEquatable<RunQueryFilterOperand>
    {
        private readonly string _value;

        /// <summary> Initializes a new instance of <see cref="RunQueryFilterOperand"/>. </summary>
        /// <exception cref="ArgumentNullException"> <paramref name="value"/> is null. </exception>
        public RunQueryFilterOperand(string value)
        {
            _value = value ?? throw new ArgumentNullException(nameof(value));
        }

        private const string PipelineNameValue = "PipelineName";
        private const string StatusValue = "Status";
        private const string RunStartValue = "RunStart";
        private const string RunEndValue = "RunEnd";
        private const string ActivityNameValue = "ActivityName";
        private const string ActivityRunStartValue = "ActivityRunStart";
        private const string ActivityRunEndValue = "ActivityRunEnd";
        private const string ActivityTypeValue = "ActivityType";
        private const string TriggerNameValue = "TriggerName";
        private const string TriggerRunTimestampValue = "TriggerRunTimestamp";
        private const string RunGroupIdValue = "RunGroupId";
        private const string LatestOnlyValue = "LatestOnly";

        /// <summary> PipelineName. </summary>
        public static RunQueryFilterOperand PipelineName { get; } = new RunQueryFilterOperand(PipelineNameValue);
        /// <summary> Status. </summary>
        public static RunQueryFilterOperand Status { get; } = new RunQueryFilterOperand(StatusValue);
        /// <summary> RunStart. </summary>
        public static RunQueryFilterOperand RunStart { get; } = new RunQueryFilterOperand(RunStartValue);
        /// <summary> RunEnd. </summary>
        public static RunQueryFilterOperand RunEnd { get; } = new RunQueryFilterOperand(RunEndValue);
        /// <summary> ActivityName. </summary>
        public static RunQueryFilterOperand ActivityName { get; } = new RunQueryFilterOperand(ActivityNameValue);
        /// <summary> ActivityRunStart. </summary>
        public static RunQueryFilterOperand ActivityRunStart { get; } = new RunQueryFilterOperand(ActivityRunStartValue);
        /// <summary> ActivityRunEnd. </summary>
        public static RunQueryFilterOperand ActivityRunEnd { get; } = new RunQueryFilterOperand(ActivityRunEndValue);
        /// <summary> ActivityType. </summary>
        public static RunQueryFilterOperand ActivityType { get; } = new RunQueryFilterOperand(ActivityTypeValue);
        /// <summary> TriggerName. </summary>
        public static RunQueryFilterOperand TriggerName { get; } = new RunQueryFilterOperand(TriggerNameValue);
        /// <summary> TriggerRunTimestamp. </summary>
        public static RunQueryFilterOperand TriggerRunTimestamp { get; } = new RunQueryFilterOperand(TriggerRunTimestampValue);
        /// <summary> RunGroupId. </summary>
        public static RunQueryFilterOperand RunGroupId { get; } = new RunQueryFilterOperand(RunGroupIdValue);
        /// <summary> LatestOnly. </summary>
        public static RunQueryFilterOperand LatestOnly { get; } = new RunQueryFilterOperand(LatestOnlyValue);
        /// <summary> Determines if two <see cref="RunQueryFilterOperand"/> values are the same. </summary>
        public static bool operator ==(RunQueryFilterOperand left, RunQueryFilterOperand right) => left.Equals(right);
        /// <summary> Determines if two <see cref="RunQueryFilterOperand"/> values are not the same. </summary>
        public static bool operator !=(RunQueryFilterOperand left, RunQueryFilterOperand right) => !left.Equals(right);
        /// <summary> Converts a string to a <see cref="RunQueryFilterOperand"/>. </summary>
        public static implicit operator RunQueryFilterOperand(string value) => new RunQueryFilterOperand(value);

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public override bool Equals(object obj) => obj is RunQueryFilterOperand other && Equals(other);
        /// <inheritdoc />
        public bool Equals(RunQueryFilterOperand other) => string.Equals(_value, other._value, StringComparison.InvariantCultureIgnoreCase);

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public override int GetHashCode() => _value?.GetHashCode() ?? 0;
        /// <inheritdoc />
        public override string ToString() => _value;
    }
}