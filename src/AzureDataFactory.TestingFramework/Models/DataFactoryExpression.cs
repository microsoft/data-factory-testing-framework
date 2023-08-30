using AzureDataFactory.TestingFramework.Functions;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models;

public partial class DataFactoryExpression
{
    public TType Evaluate<TType>(PipelineRunState state)
    {
        return FunctionPart.Parse(Value).Evaluate<TType>(state);
    }
}