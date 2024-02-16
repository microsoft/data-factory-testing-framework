import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.state import RunParameterType
from data_factory_testing_framework.state.run_parameter import RunParameter


def test_batch_job_pipeline(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(
        framework_type=TestFrameworkType.DataFactory, root_folder_path=request.fspath.dirname
    )
    pipeline = test_framework.repository.get_pipeline_by_name("batch_job")

    # Act
    activities = test_framework.evaluate_pipeline(
        pipeline,
        [
            RunParameter(RunParameterType.Pipeline, "BatchPoolId", "batch-pool-id"),
            RunParameter(RunParameterType.Pipeline, "WorkloadApplicationPackageName", "test-application"),
            RunParameter(RunParameterType.Pipeline, "WorkloadApplicationPackageVersion", "1.5.0"),
            RunParameter(RunParameterType.Pipeline, "ManagerApplicationPackageName", "batchmanager"),
            RunParameter(RunParameterType.Pipeline, "ManagerApplicationPackageVersion", "2.0.0"),
            RunParameter(
                RunParameterType.Pipeline,
                "ManagerTaskParameters",
                "--parameter1 dummy --parameter2 another-dummy",
            ),
            RunParameter(RunParameterType.Pipeline, "JobId", "802100a5-ec79-4a52-be62-8d6109f3ff9a"),
            RunParameter(RunParameterType.Pipeline, "TaskOutputFolderPrefix", "TASKOUTPUT_"),
            RunParameter(
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityName",
                "test-application-identity-name",
            ),
            RunParameter(
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityClientId",
                "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name",
            ),
            RunParameter(RunParameterType.Pipeline, "JobAdditionalEnvironmentSettings", []),
            RunParameter(
                RunParameterType.Pipeline,
                "OutputStorageAccountName",
                "test-application-output-storage-account-name",
            ),
            RunParameter(RunParameterType.Pipeline, "OutputContainerName", "test-application-output-container-name"),
            RunParameter(RunParameterType.Pipeline, "OutputFolderName", "TEMP"),
            RunParameter(RunParameterType.Pipeline, "BatchJobTimeout", "PT4H"),
            RunParameter(RunParameterType.Global, "BatchStorageAccountName", "batch-account-name"),
            RunParameter(RunParameterType.Global, "BatchAccountSubscription", "SUBSCRIPTION_ID"),
            RunParameter(RunParameterType.Global, "BatchAccountResourceGroup", "RESOURCE_GROUP"),
            RunParameter(RunParameterType.Global, "BatchURI", "https://batch-account-name.westeurope.batch.azure.com"),
            RunParameter(RunParameterType.Global, "ADFSubscription", "bd19dba4-89ad-4976-b862-848bf43a4340"),
            RunParameter(RunParameterType.Global, "ADFResourceGroup", "adf-rg"),
            RunParameter(RunParameterType.Global, "ADFName", "adf-name"),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.name == "Set UserAssignedIdentityReference"
    assert activity.type_properties["variableName"] == "UserAssignedIdentityReference"
    assert (
        activity.type_properties["value"].result
        == "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"  # noqa: E501
    )

    activity = next(activities)
    assert activity.name == "Set ManagerApplicationPackagePath"
    assert activity.type_properties["variableName"] == "ManagerApplicationPackagePath"
    assert activity.type_properties["value"].result == "$AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz"

    activity = next(activities)
    assert activity.name == "Set WorkloadApplicationPackagePath"
    assert activity.type_properties["variableName"] == "WorkloadApplicationPackagePath"
    assert (
        activity.type_properties["value"].result
        == "$AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz"
    )

    activity = next(activities)
    assert activity.name == "Set CommonEnvironmentSettings"
    assert activity.type_properties["variableName"] == "CommonEnvironmentSettings"

    common_environment_settings = activity.type_properties["value"].result
    assert len(common_environment_settings) == 8
    assert common_environment_settings[0]["name"] == "WORKLOAD_APP_PACKAGE"
    assert common_environment_settings[0]["value"] == "test-application"
    assert common_environment_settings[1]["name"] == "WORKLOAD_APP_PACKAGE_VERSION"
    assert common_environment_settings[1]["value"] == "1.5.0"
    assert common_environment_settings[2]["name"] == "MANAGER_APP_PACKAGE"
    assert common_environment_settings[2]["value"] == "batchmanager"
    assert common_environment_settings[3]["name"] == "MANAGER_APP_PACKAGE_VERSION"
    assert common_environment_settings[3]["value"] == "2.0.0"
    assert common_environment_settings[4]["name"] == "BATCH_JOB_TIMEOUT"
    assert common_environment_settings[4]["value"] == "PT4H"
    assert common_environment_settings[5]["name"] == "WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME"
    assert common_environment_settings[5]["value"] == "batch-account-name"
    assert common_environment_settings[6]["name"] == "WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID"
    assert (
        common_environment_settings[6]["value"]
        == "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"  # noqa: E501
    )
    assert common_environment_settings[7]["name"] == "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID"
    assert (
        common_environment_settings[7]["value"]
        == "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"  # noqa: E501
    )

    activity = next(activities)
    assert activity.name == "Set JobContainerName"
    assert activity.type_properties["variableName"] == "JobContainerName"
    assert activity.type_properties["value"].result == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a"

    activity = next(activities)
    assert activity.name == "Set Job Container URL"
    assert activity.type_properties["variableName"] == "JobContainerURL"
    assert (
        activity.type_properties["value"].result
        == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a"
    )

    activity = next(activities)
    assert activity.name == "Create Job Storage Container"
    assert (
        activity.type_properties["url"].result
        == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container"
    )
    assert activity.type_properties["method"] == "PUT"
    assert activity.type_properties["body"].result == "{}"

    activity = next(activities)
    assert activity.name == "Start Job"
    assert (
        activity.type_properties["url"].result
        == "https://batch-account-name.westeurope.batch.azure.com/jobs?api-version=2022-10-01.16.0"
    )
    assert activity.type_properties["method"] == "POST"

    body = activity.type_properties["body"].get_json_value()
    assert body["id"] == "802100a5-ec79-4a52-be62-8d6109f3ff9a"
    assert body["priority"] == 100
    assert body["constraints"]["maxWallClockTime"] == "PT4H"
    assert body["constraints"]["maxTaskRetryCount"] == 0
    job_manager_task = body["jobManagerTask"]
    assert job_manager_task["id"] == "Manager"
    assert job_manager_task["displayName"] == "Manager"
    assert job_manager_task["authenticationTokenSettings"]["access"] == ["job"]
    assert (
        job_manager_task["commandLine"]
        == '/bin/bash -c "python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz && python3 -m test-application job --parameter1 dummy --parameter2 another-dummy"'  # noqa: E501
    )
    application_package_references = job_manager_task["applicationPackageReferences"]
    assert len(application_package_references) == 2
    assert application_package_references[0]["applicationId"] == "batchmanager"
    assert application_package_references[0]["version"] == "2.0.0"
    assert application_package_references[1]["applicationId"] == "test-application"
    assert application_package_references[1]["version"] == "1.5.0"
    output_files = job_manager_task["outputFiles"]
    assert len(output_files) == 1
    assert (
        output_files[0]["destination"]["container"]["containerUrl"]
        == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a"
    )
    assert (
        output_files[0]["destination"]["container"]["identityReference"]["resourceId"]
        == "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"  # noqa: E501
    )
    assert output_files[0]["destination"]["container"]["path"] == "Manager/$TaskLog"
    assert output_files[0]["filePattern"] == "../*.txt"
    assert output_files[0]["uploadOptions"]["uploadCondition"] == "taskcompletion"
    assert len(job_manager_task["environmentSettings"]) == 0
    assert job_manager_task["requiredSlots"] == 1
    assert job_manager_task["killJobOnCompletion"] is False
    assert job_manager_task["userIdentity"]["username"] is None
    assert job_manager_task["userIdentity"]["autoUser"]["scope"] == "pool"
    assert job_manager_task["userIdentity"]["autoUser"]["elevationLevel"] == "nonadmin"
    assert job_manager_task["runExclusive"] is True
    assert job_manager_task["allowLowPriorityNode"] is True
    assert body["poolInfo"]["poolId"] == "batch-pool-id"
    assert body["onAllTasksComplete"] == "terminatejob"
    assert body["onTaskFailure"] == "noaction"
    assert body["usesTaskDependencies"] is True
    assert len(body["commonEnvironmentSettings"]) == 8
    common_environment_settings = body["commonEnvironmentSettings"]
    assert common_environment_settings[0]["name"] == "WORKLOAD_APP_PACKAGE"
    assert common_environment_settings[0]["value"] == "test-application"
    assert common_environment_settings[1]["name"] == "WORKLOAD_APP_PACKAGE_VERSION"
    assert common_environment_settings[1]["value"] == "1.5.0"

    activity = next(activities)
    assert activity.name == "Monitor Batch Job"
    assert activity.type_properties["pipeline"]["referenceName"] == "monitor_batch_job"
    assert len(activity.type_properties["parameters"]) == 1
    assert activity.type_properties["parameters"]["JobId"].result == "802100a5-ec79-4a52-be62-8d6109f3ff9a"

    activity = next(activities)
    assert activity.name == "Copy Output Files"
    assert activity.type_properties["pipeline"]["referenceName"] == "copy_output_files"
    assert len(activity.type_properties["parameters"]) == 5
    assert (
        activity.type_properties["parameters"]["JobContainerName"].result == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a"
    )
    assert activity.type_properties["parameters"]["TaskOutputFolderPrefix"].result == "TASKOUTPUT_"
    assert (
        activity.type_properties["parameters"]["OutputStorageAccountName"].result
        == "test-application-output-storage-account-name"
    )
    assert (
        activity.type_properties["parameters"]["OutputContainerName"].result == "test-application-output-container-name"
    )
    assert activity.type_properties["parameters"]["OutputFolderName"].result == "TEMP"

    activity = next(activities)
    assert activity.name == "Delete Job Storage Container"
    assert (
        activity.type_properties["url"].result
        == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container"
    )
    assert activity.type_properties["method"] == "DELETE"

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
