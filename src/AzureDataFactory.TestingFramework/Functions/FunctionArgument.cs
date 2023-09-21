// Copyright (c) Microsoft Corporation.

using AzureDataFactory.TestingFramework.Expressions;
using AzureDataFactory.TestingFramework.Extensions;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Functions;

public class FunctionArgument : IFunctionPart
{
    public FunctionArgument(string expression)
    {
        _expression = expression.Trim('\n').Trim(' ');
    }

    private readonly string _expression;
    public string ExpressionValue => _expression;

    public TType Evaluate<TType>(RunState state)
    {
        var evalExpression = _expression;
        var expressions = new List<BaseExpression>()
            .Concat(ActivityExpression.Find(evalExpression))
            .Concat(ParameterExpression.Find(evalExpression, ParameterType.Global))
            .Concat(ParameterExpression.Find(evalExpression, ParameterType.Parameter))
            .Concat(VariableExpression.Find(evalExpression))
            .Concat(IterationItemExpression.Find(evalExpression))
            .Concat(DatasetExpression.Find(evalExpression))
            .Concat(LinkedServiceExpression.Find(evalExpression));

        foreach (var expression in expressions)
        {
            var evaluatedExpression = expression switch
            {
                IRunExpression runExpression => runExpression.Evaluate<TType>(state),
                IPipelineExpression pipelineExpression when state is PipelineRunState pipelineRunState => pipelineExpression.Evaluate<TType>(pipelineRunState),
                _ => throw new ArgumentException($"The expression is not supported in the given context.")
            };

            // To keep the evaluatedExpression type, it is immediately returned if the expression is the only one in the string.
            if (evalExpression == expression.ExpressionValue)
                return evaluatedExpression;

            evalExpression = evalExpression.Replace(expression.ExpressionValue, evaluatedExpression.ToString());
        }

        return typeof(TType) switch
        {
            { } type when type == typeof(bool) && bool.TryParse(evalExpression, out var boolValue) => (TType)(object)boolValue,
            { } type when type == typeof(int) && int.TryParse(evalExpression, out var intValue) => (TType)(object)intValue,
            { } type when type == typeof(long) && long.TryParse(evalExpression, out var longValue) => (TType)(object)longValue,
            { } type when type == typeof(string) => (TType)(object)evalExpression.TrimOneChar('\''),
            { } type => throw new ArgumentException($"The result {evalExpression} with DataType: {type} could not be parsed accordingly.")
        };
    }
}