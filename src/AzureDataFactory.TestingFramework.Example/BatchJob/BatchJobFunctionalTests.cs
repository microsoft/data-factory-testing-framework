// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using AzureDataFactory.TestingFramework.Exceptions;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;

namespace AzureDataFactory.TestingFramework.Example.BatchJob;

public class BatchJobFunctionalTests
{

    [Fact]
    public void BatchJobTest()
    {
        var pipeline = PipelineFactory.ParseFromFile("BatchJob/pipeline.json");
        Assert.Equal("batch_job", pipeline.Name);
        Assert.Equal(11, pipeline.Activities.Count);

        var activities = pipeline.EvaluateWithActivityEnumerator(new List<IRunParameter>
        {
            new RunParameter<string>(ParameterType.Parameter, "BatchPoolId", "batch-pool-id"),
            new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageName", "test-application"),
            new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageVersion", "1.5.0"),
            new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageName", "batchmanager"),
            new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageVersion", "2.0.0"),
            new RunParameter<string>(ParameterType.Parameter, "ManagerTaskParameters", "--parameter1 dummy --parameter2 another-dummy"),
            new RunParameter<string>(ParameterType.Parameter, "JobId", "802100a5-ec79-4a52-be62-8d6109f3ff9a"),
            new RunParameter<string>(ParameterType.Parameter, "TaskOutputFolderPrefix", "TASKOUTPUT_"),
            new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityName", "test-application-identity-name"),
            new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityClientId", "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"),
            new RunParameter<string>(ParameterType.Parameter, "JobAdditionalEnvironmentSettings", "[]"),
            new RunParameter<string>(ParameterType.Parameter, "OutputStorageAccountName", "test-application-output-storage-account-name"),
            new RunParameter<string>(ParameterType.Parameter, "OutputContainerName", "test-application-output-container-name"),
            new RunParameter<string>(ParameterType.Parameter, "OutputFolderName", "TEMP"),
            new RunParameter<string>(ParameterType.Parameter, "BatchJobTimeout", "PT4H"),
            new RunParameter<string>(ParameterType.Global, "BatchStorageAccountName", "batch-account-name"),
            new RunParameter<string>(ParameterType.Global, "BatchAccountSubscription", "SUBSCRIPTION_ID"),
            new RunParameter<string>(ParameterType.Global, "BatchAccountResourceGroup", "RESOURCE_GROUP"),
            new RunParameter<string>(ParameterType.Global, "BatchURI", "https://batch-account-name.westeurope.batch.azure.com"),
            new RunParameter<string>(ParameterType.Global, "ADFSubscription", "bd19dba4-89ad-4976-b862-848bf43a4340"),
            new RunParameter<string>(ParameterType.Global, "ADFResourceGroup", "adf-rg"),
            new RunParameter<string>(ParameterType.Global, "ADFName", "adf-name"),
        });

        var setUserAssignedIdentityActivity = activities.GetNext<SetVariableActivity>();
        Assert.Equal("Set UserAssignedIdentityReference", setUserAssignedIdentityActivity.Name);
        Assert.Equal("UserAssignedIdentityReference", setUserAssignedIdentityActivity.VariableName);
        Assert.Equal("/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name", setUserAssignedIdentityActivity.Value);

        var setManagerApplicationPackagePathActivity = activities.GetNext<SetVariableActivity>();
        Assert.Equal("Set ManagerApplicationPackagePath", setManagerApplicationPackagePathActivity.Name);
        Assert.Equal("ManagerApplicationPackagePath", setManagerApplicationPackagePathActivity.VariableName);
        Assert.Equal("$AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz", setManagerApplicationPackagePathActivity.Value);

        var setWorkloadApplicationPackagePathActivity = activities.GetNext<SetVariableActivity>();
        Assert.Equal("Set WorkloadApplicationPackagePath", setWorkloadApplicationPackagePathActivity.Name);
        Assert.Equal("WorkloadApplicationPackagePath", setWorkloadApplicationPackagePathActivity.VariableName);
        Assert.Equal("$AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz", setWorkloadApplicationPackagePathActivity.Value);

        var setCommonEnvironmentSettingsActivity = activities.GetNext<SetVariableActivity>();
        Assert.Equal("Set CommonEnvironmentSettings", setCommonEnvironmentSettingsActivity.Name);
        Assert.Equal("CommonEnvironmentSettings", setCommonEnvironmentSettingsActivity.VariableName);
        Assert.Equal(@"[
        {
	        ""name"": ""WORKLOAD_APP_PACKAGE"",
	        ""value"": ""test-application""
        },
        {
	        ""name"": ""WORKLOAD_APP_PACKAGE_VERSION"",
	        ""value"": ""1.5.0""
        },
        {
	        ""name"": ""MANAGER_APP_PACKAGE"",
	        ""value"": ""batchmanager""
        },
        {
	        ""name"": ""MANAGER_APP_PACKAGE_VERSION"",
	        ""value"": ""2.0.0""
        },
        {
	        ""name"": ""BATCH_JOB_TIMEOUT"",
	        ""value"": ""PT4H""
        },
        {
	        ""name"": ""WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME"",
	        ""value"": ""batch-account-name""
        },
        {
	        ""name"": ""WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID"",
	        ""value"": ""/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name""
        },
        {
	        ""name"": ""WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID"",
	        ""value"": ""/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name""
        }
        ]", setCommonEnvironmentSettingsActivity.Value, ignoreLineEndingDifferences: true, ignoreWhiteSpaceDifferences: true);

        var setJobContainerNameActivity = activities.GetNext<SetVariableActivity>();
        Assert.Equal("Set JobContainerName", setJobContainerNameActivity.Name);
        Assert.Equal("JobContainerName", setJobContainerNameActivity.VariableName);
        Assert.Equal("job-802100a5-ec79-4a52-be62-8d6109f3ff9a", setJobContainerNameActivity.Value);

        var setJobContainerUrlActivity = activities.GetNext<SetVariableActivity>();
        Assert.Equal("Set Job Container URL", setJobContainerUrlActivity.Name);
        Assert.Equal("JobContainerURL", setJobContainerUrlActivity.VariableName);
        Assert.Equal("https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a", setJobContainerUrlActivity.Value);

        var createJobContainer = activities.GetNext<WebActivity>();
        Assert.Equal("Create Job Storage Container", createJobContainer.Name);
        Assert.Equal("https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container", createJobContainer.Uri);
        Assert.Equal("PUT", createJobContainer.Method);
        Assert.Equal("{}", createJobContainer.Body);

        var startJobActivity = activities.GetNext<WebActivity>();
        Assert.Equal("Start Job", startJobActivity.Name);
        Assert.Equal("https://batch-account-name.westeurope.batch.azure.com/jobs?api-version=2022-10-01.16.0", startJobActivity.Uri);
        Assert.Equal("POST", startJobActivity.Method);
        Assert.Equal(@"{
    ""id"": ""802100a5-ec79-4a52-be62-8d6109f3ff9a"",
    ""priority"": 100,
    ""constraints"": {
        ""maxWallClockTime"":""PT4H"",
        ""maxTaskRetryCount"": 0
    },
    ""jobManagerTask"": {
        ""id"": ""Manager"",
        ""displayName"": ""Manager"",
        ""authenticationTokenSettings"": {
            ""access"": [
                ""job""
            ]
        },
        ""commandLine"": ""/bin/bash -c \""python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz && python3 -m test-application job --parameter1 dummy --parameter2 another-dummy\"""",
        ""applicationPackageReferences"": [
            {
                ""applicationId"": ""batchmanager"",
                ""version"": ""2.0.0""
            },
            {
                ""applicationId"": ""test-application"",
                ""version"": ""1.5.0""
            }
        ],
        ""outputFiles"": [
            {
                ""destination"": {
                    ""container"": {
                        ""containerUrl"": ""https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a"",
                        ""identityReference"": {
                            ""resourceId"": ""/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name""
                        },
                        ""path"": ""Manager/$TaskLog""
                    }
                },
                ""filePattern"": ""../*.txt"",
                ""uploadOptions"": {
                    ""uploadCondition"": ""taskcompletion""
                }
            }
        ],
        ""environmentSettings"": [],
        ""requiredSlots"": 1,
        ""killJobOnCompletion"": false,
        ""userIdentity"": {
            ""username"": null,
            ""autoUser"": {
                ""scope"": ""pool"",
                ""elevationLevel"": ""nonadmin""
            }
        },
        ""runExclusive"": true,
        ""allowLowPriorityNode"": true
    },
    ""poolInfo"": {
        ""poolId"": ""batch-pool-id""
    },
    ""onAllTasksComplete"": ""terminatejob"",
    ""onTaskFailure"": ""noaction"",
    ""usesTaskDependencies"": true,
    ""commonEnvironmentSettings"": [{""name"":""WORKLOAD_APP_PACKAGE"",""value"":""test-application""},{""name"":""WORKLOAD_APP_PACKAGE_VERSION"",""value"":""1.5.0""},{""name"":""MANAGER_APP_PACKAGE"",""value"":""batchmanager""},{""name"":""MANAGER_APP_PACKAGE_VERSION"",""value"":""2.0.0""},{""name"":""BATCH_JOB_TIMEOUT"",""value"":""PT4H""},{""name"":""WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME"",""value"":""batch-account-name""},{""name"":""WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID"",""value"":""/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name""},{""name"":""WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID"",""value"":""/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name""}]}", startJobActivity.Body, ignoreLineEndingDifferences: true, ignoreWhiteSpaceDifferences: true);

        var monitorActivity = activities.GetNext<ExecutePipelineActivity>();
        Assert.Equal("Monitor Batch Job", monitorActivity.Name);
        Assert.Equal("monitor_batch_job", monitorActivity.Pipeline.ReferenceName);
        Assert.Equal(1, monitorActivity.Parameters.Count);
        Assert.Equal("802100a5-ec79-4a52-be62-8d6109f3ff9a", monitorActivity.Parameters["JobId"]);

        var copyOutputFiles = activities.GetNext<ExecutePipelineActivity>();
        Assert.Equal("Copy Output Files", copyOutputFiles.Name);
        Assert.Equal("copy_output_files", copyOutputFiles.Pipeline.ReferenceName);
        Assert.Equal(5, copyOutputFiles.Parameters.Count);
        Assert.Equal("job-802100a5-ec79-4a52-be62-8d6109f3ff9a", copyOutputFiles.Parameters["JobContainerName"]);
        Assert.Equal("TASKOUTPUT_", copyOutputFiles.Parameters["TaskOutputFolderPrefix"]);
        Assert.Equal("test-application-output-storage-account-name", copyOutputFiles.Parameters["OutputStorageAccountName"]);
        Assert.Equal("test-application-output-container-name", copyOutputFiles.Parameters["OutputContainerName"]);
        Assert.Equal("TEMP", copyOutputFiles.Parameters["OutputFolderName"]);

        var deleteJobContainer = activities.GetNext<WebActivity>();
        Assert.Equal("Delete Job Storage Container", deleteJobContainer.Name);
        Assert.Equal("https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container", deleteJobContainer.Uri);
        Assert.Equal("DELETE", deleteJobContainer.Method);
        Assert.Null(deleteJobContainer.Body);

        Assert.Throws<ActivityEnumeratorException>(() => activities.GetNext());
    }
}