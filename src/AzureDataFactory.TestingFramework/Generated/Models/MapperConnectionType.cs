// <auto-generated/>

#nullable disable

using System.ComponentModel;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Type of connection via linked service or dataset. </summary>
    public readonly partial struct MapperConnectionType : IEquatable<MapperConnectionType>
    {
        private readonly string _value;

        /// <summary> Initializes a new instance of <see cref="MapperConnectionType"/>. </summary>
        /// <exception cref="ArgumentNullException"> <paramref name="value"/> is null. </exception>
        public MapperConnectionType(string value)
        {
            _value = value ?? throw new ArgumentNullException(nameof(value));
        }

        private const string LinkedservicetypeValue = "linkedservicetype";

        /// <summary> linkedservicetype. </summary>
        public static MapperConnectionType Linkedservicetype { get; } = new MapperConnectionType(LinkedservicetypeValue);
        /// <summary> Determines if two <see cref="MapperConnectionType"/> values are the same. </summary>
        public static bool operator ==(MapperConnectionType left, MapperConnectionType right) => left.Equals(right);
        /// <summary> Determines if two <see cref="MapperConnectionType"/> values are not the same. </summary>
        public static bool operator !=(MapperConnectionType left, MapperConnectionType right) => !left.Equals(right);
        /// <summary> Converts a string to a <see cref="MapperConnectionType"/>. </summary>
        public static implicit operator MapperConnectionType(string value) => new MapperConnectionType(value);

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public override bool Equals(object obj) => obj is MapperConnectionType other && Equals(other);
        /// <inheritdoc />
        public bool Equals(MapperConnectionType other) => string.Equals(_value, other._value, StringComparison.InvariantCultureIgnoreCase);

        /// <inheritdoc />
        [EditorBrowsable(EditorBrowsableState.Never)]
        public override int GetHashCode() => _value?.GetHashCode() ?? 0;
        /// <inheritdoc />
        public override string ToString() => _value;
    }
}
