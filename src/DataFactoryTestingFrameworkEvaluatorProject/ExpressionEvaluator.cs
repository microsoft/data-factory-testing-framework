namespace DataFactoryTestingFrameworkEvaluator;

using Microsoft.Azure.Workflows.Templates.Expressions;
using Microsoft.Azure.Workflows.Templates.Helpers;
using Newtonsoft.Json.Linq;
using Microsoft.WindowsAzure.ResourceStack.Common.Collections;
using Microsoft.WindowsAzure.ResourceStack.Common.Instrumentation;
using System.Reflection;

public class ExpressionEvaluator
{
    private TemplateExpressionEvaluationHelper GetTemplateFunctionEvaluationHelper(string parametersJson, string variablesJson, string itemValueJson)
    {
        var variables = ParseJsonToInsensitiveDictionary(variablesJson);
        var parameterValues = ParseJsonToInsensitiveDictionary(parametersJson);
        var itemValue = JToken.Parse(itemValueJson);

        var helper = TemplateExpressionsHelper.GetTemplateFunctionEvaluationHelper(
        parameterValues: parameterValues,
        onGetApplicationConfiguration: delegate (string key)
        {
            return null;
        },
        triggerName: "triggerName",
        triggerValue: "triggerValue",
        enablePreserveAnnotations: true,
        actionValues: new InsensitiveDictionary<JToken>(),
        resultValues: new InsensitiveDictionary<JToken>(),
        actionIsForeachValues: new InsensitiveDictionary<bool>(),
        actionHasNonReferenceableAggregatedPartialContentValues: new InsensitiveDictionary<bool>(),
        workflowValue: new JObject(),
        variables: variables,
        itemValue: itemValue,
        itemValues: new InsensitiveDictionary<JToken>(),
        iterationIndexes: new InsensitiveDictionary<JToken>(),
        secretValues: new InsensitiveDictionary<JToken>(),
        dependencyTrackingContext: null
        );

        return helper;
    }

    private InsensitiveDictionary<JToken> ParseJsonToInsensitiveDictionary(string json)
    {
        var jObject = JObject.Parse(json);
        var insensitiveDictionary = new InsensitiveDictionary<JToken>();

        foreach (var property in jObject.Properties())
        {
            insensitiveDictionary[property.Name] = property.Value;
        }

        return insensitiveDictionary;
    }

    private void PatchRequestCorrelationContext()
    {
        var data = (RequestCorrelationContext)new RequestCorrelationContext();
        data.SetContentVersion("2016-04-01-preview");

        TypeInfo? typeInfo = typeof(RequestCorrelationContext).GetNestedType("CallContext", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static) as System.Reflection.TypeInfo;
        var methodInfoLogicalSetData = typeInfo.GetMethod("LogicalSetData");
        methodInfoLogicalSetData.Invoke(null, new object[] { RequestCorrelationContext.PropertyRequestCorrelationContext, data });
    }

    public string EvaluateExpression(string expression, string parametersJson, string variablesJson, string itemValueJson)
    {
        var helper = GetTemplateFunctionEvaluationHelper(parametersJson, variablesJson, itemValueJson);
        var context = new TemplateExpressionEvaluationContext(helper);
        this.PatchRequestCorrelationContext();

        // Return the evaluated expression as a json object:
        var result = TemplateExpressionsHelper.EvaluateTemplateLanguageExpression(expression, context);

        var resultObject = new JObject();
        resultObject.Add("result", result);
        return resultObject.ToString();
    }
}
