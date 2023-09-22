// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace AzureDataFactory.TestingFramework.Functions;

public static class TypeHelper
{
    public static object ConvertListGenericTypeToType(List<object> value, Type type)
    {
        var enumerableType = typeof(Enumerable);
        var castMethod = enumerableType.GetMethod(nameof(Enumerable.Cast)).MakeGenericMethod(type);
        var toListMethod = enumerableType.GetMethod(nameof(Enumerable.ToList)).MakeGenericMethod(type);

        var items = value.Select(item => Convert.ChangeType(item, type)).ToList();

        var castedItems = castMethod.Invoke(null, new[] { items });

        return toListMethod.Invoke(null, new[] { castedItems });
    }
}