// <auto-generated/>

#nullable disable

using System.ComponentModel;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Status result of the activity when the state is set to Inactive. This is an optional property and if not provided when the activity is inactive, the status will be Succeeded by default. </summary>
    public readonly partial struct ActivityOnInactiveMarkAs : IEquatable<ActivityOnInactiveMarkAs>
    {
        private readonly string _value;

        /// <summary> Initializes a new instance of <see cref="ActivityOnInactiveMarkAs"/>. </summary>
        /// <exception cref="ArgumentNullException"> <paramref name="value"/> is null. </exception>
        public ActivityOnInactiveMarkAs(string value)
        {
            _value = value ?? throw new ArgumentNullException(nameof(value));
        }

        private const string SucceededValue = "Succeeded";
        private const string FailedValue = "Failed";
        private const string SkippedValue = "Skipped";

        /// <summary> Succeeded. </summary>
        public static ActivityOnInactiveMarkAs Succeeded { get; } = new ActivityOnInactiveMarkAs(SucceededValue);
        /// <summary> Failed. </summary>
        public static ActivityOnInactiveMarkAs Failed { get; } = new ActivityOnInactiveMarkAs(FailedValue);
        /// <summary> Skipped. </summary>
        public static ActivityOnInactiveMarkAs Skipped { get; } = new ActivityOnInactiveMarkAs(SkippedValue);
        /// <summary> Determines if two <see cref="ActivityOnInactiveMarkAs"/> values are the same. </summary>
        public static bool operator ==(ActivityOnInactiveMarkAs left, ActivityOnInactiveMarkAs right) => left.Equals(right);
        /// <summary> Determines if two <see cref="ActivityOnInactiveMarkAs"/> values are not the same. </summary>
        public static bool operator !=(ActivityOnInactiveMarkAs left, ActivityOnInactiveMarkAs right) => !left.Equals(right);
        /// <summary> Converts a string to a <see cref="ActivityOnInactiveMarkAs"/>. </summary>
        public static implicit operator ActivityOnInactiveMarkAs(string value) => new ActivityOnInactiveMarkAs(value);

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public override bool Equals(object obj) => obj is ActivityOnInactiveMarkAs other && Equals(other);
        /// <inheritdoc />
        public bool Equals(ActivityOnInactiveMarkAs other) => string.Equals(_value, other._value, StringComparison.InvariantCultureIgnoreCase);

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public override int GetHashCode() => _value?.GetHashCode() ?? 0;
        /// <inheritdoc />
        public override string ToString() => _value;
    }
}
