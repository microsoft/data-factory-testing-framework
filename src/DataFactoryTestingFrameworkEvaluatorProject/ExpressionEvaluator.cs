namespace DataFactoryTestingFrameworkEvaluator;

using Microsoft.Azure.Workflows.Templates.Expressions;
using Microsoft.Azure.Workflows.Templates.Helpers;
using Newtonsoft.Json.Linq;
using Microsoft.WindowsAzure.ResourceStack.Common.Collections;
using Microsoft.WindowsAzure.ResourceStack.Common.Instrumentation;
using System.Reflection;

public class ExpressionEvaluator
{
    private InsensitiveDictionary<JToken> parameterValues;
    private InsensitiveDictionary<JToken> variables;
    private JToken? itemValue;


    public ExpressionEvaluator()
    {
        this.parameterValues = new InsensitiveDictionary<JToken>();
        this.variables = new InsensitiveDictionary<JToken>();
        this.itemValue = null;
    }


    private TemplateExpressionEvaluationHelper GetTemplateFunctionEvaluationHelper()
    {
        var helper = TemplateExpressionsHelper.GetTemplateFunctionEvaluationHelper(
            parameterValues: this.parameterValues,
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
            variables: this.variables,
            itemValue: this.itemValue,
            itemValues: new InsensitiveDictionary<JToken>(),
            iterationIndexes: new InsensitiveDictionary<JToken>(),
            secretValues: new InsensitiveDictionary<JToken>(),
            dependencyTrackingContext: null
            );

        return helper;
    }

    /// <summary>
    /// Set the parameters from a json string
    /// </summary>
    /// <param name="json"></param>
    public void SetParametersFromJson(string json)
    {
        var jObject = JObject.Parse(json);
        foreach (var property in jObject.Properties())
        {
            this.parameterValues[property.Name] = property.Value;
        }
    }

    /// <summary>
    /// Set the variables from a json string
    /// </summary>
    /// <param name="json"></param>
    /// <returns></returns>
    public void SetVariablesFromJson(string json)
    {
        var jObject = JObject.Parse(json);
        foreach (var property in jObject.Properties())
        {
            this.variables[property.Name] = property.Value;
        }
    }

    /// <summary>
    /// Set the item value from a json string
    /// </summary>
    /// <param name="json"></param>
    public void SetItemValueFromJson(string json)
    {
        this.itemValue = JToken.Parse(json);
    }

    private void PatchRequestCorrelationContext()
    {
        var data = (RequestCorrelationContext)new RequestCorrelationContext();
        data.SetContentVersion("2016-04-01-preview");

        TypeInfo? typeInfo = typeof(RequestCorrelationContext).GetNestedType("CallContext", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static) as System.Reflection.TypeInfo;
        var methodInfoLogicalSetData = typeInfo.GetMethod("LogicalSetData");
        methodInfoLogicalSetData.Invoke(null, new object[] { RequestCorrelationContext.PropertyRequestCorrelationContext, data });
    }

    public string EvaluateExpression(string expression)
    {
        var helper = GetTemplateFunctionEvaluationHelper();
        var context = new TemplateExpressionEvaluationContext(helper);
        this.PatchRequestCorrelationContext();

        // Return the evaluated expression as a json object:
        var result = TemplateExpressionsHelper.EvaluateTemplateLanguageExpression(expression, context);

        var resultObject = new JObject();
        resultObject.Add("result", result);
        return resultObject.ToString();
    }
}
