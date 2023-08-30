using System.Collections;
using Azure.Core.Expressions.DataFactory;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Models.Base;

public abstract class DataFactoryEntity
{
    public virtual DataFactoryEntity Evaluate(PipelineRunState state)
    {
        EvaluateProperties(this, state, new List<object>());

        return this;
    }

    private static void EvaluateProperties(object currentObject, PipelineRunState state, List<object> visited)
    {
        if (visited.Contains(currentObject))
            return;

        visited.Add(currentObject);

        if (currentObject is string or DataFactoryExpression || currentObject.GetType().IsPrimitive)
            return;

        // Loop through all properties of the type properties, evaluate them and loop through child properties
        foreach (var property in currentObject.GetType().GetProperties())
        {
            if (property.PropertyType.IsPrimitive || property.PropertyType == typeof(string) || property.PropertyType == typeof(List<string>))
                continue;

            var propertyValue = property.GetValue(currentObject);

            if (propertyValue is null)
                continue;

            if (propertyValue is DataFactoryElement<string> stringDataFactoryElement)
            {
                stringDataFactoryElement.Evaluate(state);
                continue;
            }

            if (propertyValue is DataFactoryElement<int> intDataFactoryElement)
            {
                intDataFactoryElement.Evaluate(state);
                continue;
            }

            if (propertyValue is DataFactoryElement<bool> boolDataFactoryElement)
            {
                boolDataFactoryElement.Evaluate(state);
                continue;
            }

            if (propertyValue is Dictionary<string, object> dictionary)
            {
                foreach (var item in dictionary)
                    EvaluateProperties(item.Value, state, visited);
            }
            else if (propertyValue is IEnumerable enumerable)
            {
                foreach (var item in enumerable)
                {
                    if (item is DataFactoryEntity)
                        continue;

                    EvaluateProperties(item, state, visited);
                }
            }
            else
            {
                EvaluateProperties(propertyValue, state, visited);
            }
        }
    }
}