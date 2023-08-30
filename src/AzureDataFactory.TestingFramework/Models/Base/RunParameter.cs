namespace AzureDataFactory.TestingFramework.Models.Base;

public interface IRunParameter
{
    public string Name { get; }
    public ParameterType Type { get; }
}
public class RunParameter<TValueType> : IRunParameter
{
    public RunParameter(ParameterType type, string name, TValueType value)
    {
        Name = name;
        Type = type;
        Value = value;
    }

    public string Name { get; }
    public ParameterType Type { get; }
    public TValueType Value { get; }
}