using Azure.ResourceManager.DataFactory;
using AzureDataFactory.TestingFramework.Models;
using AzureDataFactory.TestingFramework.Models.Base;
using AzureDataFactory.TestingFramework.Models.Pipelines;
using ParameterType = AzureDataFactory.TestingFramework.Models.Base.ParameterType;

namespace AzureDataFactory.TestingFramework.Example.BatchJob;

public class BatchJobUnitTests
{
    private readonly Pipeline _pipeline;
    private readonly PipelineRunState _state;

    public BatchJobUnitTests()
    {
        _pipeline = PipelineFactory.ParseFromFile("BatchJob/pipeline.json");
        _state = new PipelineRunState();
    }


    [Fact]
    public void SetJobContainerUrlTest()
    {
	    // Arrange
        var activity = _pipeline.GetActivityByName("Set Job Container URL") as SetVariableActivity;
        var variable = new PipelineRunVariable<string>("JobContainerURL");
        _state.Variables.Add(new PipelineRunVariable<string>("JobContainerName", "job-8b6b545b-c583-4a06-adf7-19ff41370aba"));
        _state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchStorageAccountName", "batch-account-name"));
        _state.Variables.Add(variable);

        // Act
        activity.Evaluate(_state);

        // Assert
        var expectedUrl = "https://batch-account-name.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba";
        Assert.Equal(expectedUrl, activity.Value);
        Assert.Equal(expectedUrl, variable.Value);
    }

    [Fact]
    public void SetUserAssignedIdentityReferenceTests()
    {
	    // Arrange
		var activity = _pipeline.GetActivityByName("Set UserAssignedIdentityReference") as SetVariableActivity;
		var variable = new PipelineRunVariable<string>("UserAssignedIdentityReference");
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchAccountSubscription", "batch-account-subscription"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchAccountResourceGroup", "batch-account-resource-group"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityName", "workload-user-assigned-identity-name"));
		_state.Variables.Add(variable);

		// Act
		activity.Evaluate(_state);

		// Assert
		var expectedReference = "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name";
		Assert.Equal(expectedReference, activity.Value);
		Assert.Equal(expectedReference, variable.Value);
    }

    [Fact]
    public void SetManagerApplicationPackagePathTest()
    {
	    // Arrange
	    var activity = _pipeline.GetActivityByName("Set ManagerApplicationPackagePath") as SetVariableActivity;
	    var variable = new PipelineRunVariable<string>("ManagerApplicationPackagePath");
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageName", "managerworkload"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageVersion", "0.13.2"));
	    _state.Variables.Add(variable);

	    // Act
	    activity.Evaluate(_state);

	    // Assert
	    var expectedPath = "$AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz";
	    Assert.Equal(expectedPath, activity.Value);
    }

    [Fact]
    public void SetWorkloadApplicationPackagePathTest()
	{
	    // Arrange
	    var activity = _pipeline.GetActivityByName("Set WorkloadApplicationPackagePath") as SetVariableActivity;
	    var variable = new PipelineRunVariable<string>("WorkloadApplicationPackagePath");
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageName", "workload"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageVersion", "0.13.2"));
	    _state.Variables.Add(variable);

	    // Act
	    activity.Evaluate(_state);

	    // Assert
	    var expectedPath = "$AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz";
	    Assert.Equal(expectedPath, activity.Value);
	}

    [Fact]
    public void SetCommonEnvironmentSettingsTest()
    {
	    // Arrange
	    var activity = _pipeline.GetActivityByName("Set CommonEnvironmentSettings") as SetVariableActivity;
	    var variable = new PipelineRunVariable<string>("CommonEnvironmentSettings");
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageName", "workload"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageVersion", "0.13.2"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageName", "managerworkload"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageVersion", "0.13.2"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "BatchJobTimeout", "PT4H"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchStorageAccountName", "batch-account-name"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityName", "workload-user-assigned-identity-name"));
	    _state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityClientId", "workload-user-assigned-identity-client-id"));
	    _state.Variables.Add(new PipelineRunVariable<string>("UserAssignedIdentityReference", "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"));
	    _state.Variables.Add(variable);

	    // Act
	    activity.Evaluate(_state);

	    // Assert
	    var expectedSettings = @"[
  {
    ""name"": ""WORKLOAD_APP_PACKAGE"",
	    ""value"": ""workload""
    },
    {
	    ""name"": ""WORKLOAD_APP_PACKAGE_VERSION"",
	    ""value"": ""0.13.2""
    },
    {
	    ""name"": ""MANAGER_APP_PACKAGE"",
	    ""value"": ""managerworkload""
    },
    {
	    ""name"": ""MANAGER_APP_PACKAGE_VERSION"",
	    ""value"": ""0.13.2""
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
	    ""value"": ""/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name""
    },
    {
	    ""name"": ""WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID"",
	    ""value"": ""workload-user-assigned-identity-client-id""
    }
    ]";
	    Assert.Equal(expectedSettings, activity.Value, ignoreLineEndingDifferences: true, ignoreWhiteSpaceDifferences: true);
    }

	[Fact]
	public void CreateJobStorageContainerTest()
	{
		// Arrange
		var activity = _pipeline.GetActivityByName("Create Job Storage Container") as WebActivity;
		_state.Variables.Add(new PipelineRunVariable<string>("JobContainerURL", "https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba"));

		// Act
		activity.Evaluate(_state);

		// Assert
		Assert.Equal("Create Job Storage Container", activity.Name);
		Assert.Equal("https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba?restype=container", activity.Uri);
		Assert.Equal("PUT", activity.Method);
		Assert.Equal("{}", activity.Body);
	}

	[Fact]
	public void SetJobContainerNameTest()
	{
		// Arrange
		var activity = _pipeline.GetActivityByName("Set JobContainerName") as SetVariableActivity;
		var jobContainerNameVariable = new PipelineRunVariable<string>("JobContainerName");
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "JobId", "8b6b545b-c583-4a06-adf7-19ff41370aba"));
		_state.Variables.Add(jobContainerNameVariable);

		// Act
		activity.Evaluate(_state);

		// Assert
		Assert.Equal("job-8b6b545b-c583-4a06-adf7-19ff41370aba", activity.Value);
		Assert.Equal("job-8b6b545b-c583-4a06-adf7-19ff41370aba", jobContainerNameVariable.Value);
	}

	[Fact]
	public void StartJobPipelineTest()
	{
		// Arrange
		var activity = _pipeline.GetActivityByName("Start Job") as WebActivity;
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchURI", "https://batch-account-name.westeurope.batch.azure.com"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchStorageAccountName", "batchstorage"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "ADFSubscription", "d9153e28-dd4e-446c-91e4-0b1331b523f1"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "ADFResourceGroup", "adf-rg"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "ADFName", "adf-name"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "JobId", "8b6b545b-c583-4a06-adf7-19ff41370aba"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "BatchJobTimeout", "PT4H"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "BatchPoolId", "test-application-batch-pool-id"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageName", "test-application-name"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadApplicationPackageVersion", "1.5.0"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageName", "batchmanager"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerApplicationPackageVersion", "2.0.0"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "ManagerTaskParameters", "--parameter1 dummy --parameter2 another-dummy"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityName", "test-application-batch-pool-id"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "WorkloadUserAssignedIdentityClientId", "test-application-identity-client-id"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "JobAdditionalEnvironmentSettings", "[{\"name\": \"STORAGE_ACCOUNT_NAME\", \"value\": \"teststorage\"}]"));
		_state.Variables.Add(new PipelineRunVariable<string>("JobContainerURL", "https://batch-account-name.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba"));
		_state.Variables.Add(new PipelineRunVariable<string>("UserAssignedIdentityReference", "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"));
		_state.Variables.Add(new PipelineRunVariable<string>("ManagerApplicationPackagePath", "$AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz"));
		_state.Variables.Add(new PipelineRunVariable<string>("WorkloadApplicationPackagePath", "$AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz"));
		_state.Variables.Add(new PipelineRunVariable<string>("CommonEnvironmentSettings", @"[{""name"": ""COMMON_ENV_SETTING"", ""value"":""dummy""}]"));

		// Act
		activity.Evaluate(_state);

		// Assert
		Assert.Equal("Start Job", activity.Name);
		Assert.Equal("https://batch-account-name.westeurope.batch.azure.com/jobs?api-version=2022-10-01.16.0", activity.Uri);
		Assert.Equal("POST", activity.Method);
		Assert.Equal(@"{
    ""id"": ""8b6b545b-c583-4a06-adf7-19ff41370aba"",
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
        ""commandLine"": ""/bin/bash -c \""python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz && python3 -m test-application-name job --parameter1 dummy --parameter2 another-dummy\"""",
        ""applicationPackageReferences"": [
            {
                ""applicationId"": ""batchmanager"",
                ""version"": ""2.0.0""
            },
            {
                ""applicationId"": ""test-application-name"",
                ""version"": ""1.5.0""
            }
        ],
        ""outputFiles"": [
            {
                ""destination"": {
                    ""container"": {
                        ""containerUrl"": ""https://batch-account-name.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba"",
                        ""identityReference"": {
                            ""resourceId"": ""/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name""
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
        ""poolId"": ""test-application-batch-pool-id""
    },
    ""onAllTasksComplete"": ""terminatejob"",
    ""onTaskFailure"": ""noaction"",
    ""usesTaskDependencies"": true,
    ""commonEnvironmentSettings"": [{""name"":""COMMON_ENV_SETTING"",""value"":""dummy""},{""name"":""STORAGE_ACCOUNT_NAME"",""value"":""teststorage""}]}", activity.Body, ignoreLineEndingDifferences: true, ignoreWhiteSpaceDifferences: true);
	}

	[Fact]
	public void MonitorJobTest()
	{
		// Arrange
		var activity = _pipeline.GetActivityByName("Monitor Batch Job") as ExecutePipelineActivity;
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "JobId", "8b6b545b-c583-4a06-adf7-19ff41370aba"));

		// Act
		activity.Evaluate(_state);

		// Assert
		Assert.Equal("Monitor Batch Job", activity.Name);
		Assert.Equal("monitor_batch_job", activity.Pipeline.ReferenceName);
		Assert.Equal(1, activity.Parameters.Count);
		Assert.Equal("8b6b545b-c583-4a06-adf7-19ff41370aba", activity.Parameters["JobId"]);
	}

	[Fact]
	public void CopyOutputFilesTest()
	{
		// Arrange
		var activity = _pipeline.GetActivityByName("Copy Output Files") as ExecutePipelineActivity;
		_state.Variables.Add(new PipelineRunVariable<string>("JobContainerName", "job-8b6b545b-c583-4a06-adf7-19ff41370aba"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "TaskOutputFolderPrefix", "TASKOUTPUT_"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "OutputStorageAccountName", "teststorage"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "OutputContainerName", "test-application-output-container-name"));
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Parameter, "OutputFolderName", "output"));

		// Act
		activity.Evaluate(_state);

		// Assert
		Assert.Equal("Copy Output Files", activity.Name);
		Assert.Equal("copy_output_files", activity.Pipeline.ReferenceName);
		Assert.Equal(5, activity.Parameters.Count);
		Assert.Equal("job-8b6b545b-c583-4a06-adf7-19ff41370aba", activity.Parameters["JobContainerName"]);
		Assert.Equal("TASKOUTPUT_", activity.Parameters["TaskOutputFolderPrefix"]);
		Assert.Equal("teststorage", activity.Parameters["OutputStorageAccountName"]);
		Assert.Equal("test-application-output-container-name", activity.Parameters["OutputContainerName"]);
		Assert.Equal("output", activity.Parameters["OutputFolderName"]);
	}

	[Fact]
	public void DeleteJobStorageContainerTest()
	{
		// Arrange
		var activity = _pipeline.GetActivityByName("Delete Job Storage Container") as WebActivity;
		_state.Parameters.Add(new RunParameter<string>(ParameterType.Global, "BatchStorageAccountName", "batchstorage"));
		_state.Variables.Add(new PipelineRunVariable<string>("JobContainerName", "job-8b6b545b-c583-4a06-adf7-19ff41370aba"));

		// Act
		activity.Evaluate(_state);

		// Assert
		Assert.Equal("Delete Job Storage Container", activity.Name);
		Assert.Equal("https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba?restype=container", activity.Uri);
		Assert.Equal("DELETE", activity.Method);
		Assert.Null(activity.Body);
	}
}