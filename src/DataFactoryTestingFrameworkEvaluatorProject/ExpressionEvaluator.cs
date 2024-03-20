namespace DataFactoryTestingFrameworkEvaluator;

using Microsoft.Azure.Workflows.Templates.Expressions;
using Microsoft.Azure.Workflows.Templates.Helpers;
using Newtonsoft.Json.Linq;
using Microsoft.WindowsAzure.ResourceStack.Common.Collections;
using Microsoft.WindowsAzure.ResourceStack.Common.Instrumentation;
using System.Reflection;

public class ExpressionEvaluator
{
    private TemplateExpressionEvaluationHelper GetTemplateFunctionEvaluationHelper(
        string parametersJson,
        string variablesJson,
        string itemValueJson,
        string activityValuesJson
        )
    {
        var variables = ParseJsonToInsensitiveDictionary(variablesJson);
        var parameterValues = ParseJsonToInsensitiveDictionary(parametersJson);
        var actionValues = ParseJsonToInsensitiveDictionary(activityValuesJson);
        var itemValue = itemValueJson != null ? JToken.Parse(itemValueJson) : null;

        var triggerValue = new JObject();
        var outputs = new JObject();
        triggerValue.Add("outputs", outputs);
        var param = JToken.Parse(parametersJson);
        var body = new JObject();
        outputs.Add("body", param);

        var actionHasNonReferenceableAggregatedPartialContentValues = new InsensitiveDictionary<bool>();
        // loop over all keys in actionValues and set the value to false
        foreach (var key in actionValues.Keys)
        {
            actionHasNonReferenceableAggregatedPartialContentValues.Add(key, false);
        }

        var helper = TemplateExpressionsHelper.GetTemplateFunctionEvaluationHelper(
        parameterValues: parameterValues,
        onGetApplicationConfiguration: delegate (string key)
        {
            return null;
        },
        triggerName: "triggerName",
        triggerValue: triggerValue,
        enablePreserveAnnotations: true,
        actionValues: actionValues,
        resultValues: new InsensitiveDictionary<JToken>(),
        actionIsForeachValues: new InsensitiveDictionary<bool>(),
        actionHasNonReferenceableAggregatedPartialContentValues: actionHasNonReferenceableAggregatedPartialContentValues,
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

    public string EvaluateExpression(string expression, string parametersJson, string variablesJson, string itemValueJson, string activityValuesJson)
    {
        var helper = GetTemplateFunctionEvaluationHelper(parametersJson, variablesJson, itemValueJson, activityValuesJson);
        var context = new TemplateExpressionEvaluationContext(helper);

        this.PatchRequestCorrelationContext();

        // Return the evaluated expression as a json object:
        var result = TemplateExpressionsHelper.EvaluateTemplateLanguageExpression(expression, context);

        var resultObject = new JObject();
        resultObject.Add("result", result);
        return resultObject.ToString();
    }

}
