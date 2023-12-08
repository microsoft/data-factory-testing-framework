import pytest
from data_factory_testing_framework.state import RunParameterType
from data_factory_testing_framework.state.run_parameter import RunParameter
from data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


def test_batch_job_pipeline(request: pytest.FixtureRequest) -> None:
    # Arrange
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric, root_folder_path=request.fspath.dirname)
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
            RunParameter(RunParameterType.Pipeline, "JobAdditionalEnvironmentSettings", "[]"),
            RunParameter(
                RunParameterType.Pipeline,
                "OutputStorageAccountName",
                "test-application-output-storage-account-name",
            ),
            RunParameter(RunParameterType.Pipeline, "OutputContainerName", "test-application-output-container-name"),
            RunParameter(RunParameterType.Pipeline, "OutputFolderName", "TEMP"),
            RunParameter(RunParameterType.Pipeline, "BatchJobTimeout", "PT4H"),
            RunParameter(RunParameterType.Pipeline, "BatchStorageAccountName", "batch-account-name"),
            RunParameter(RunParameterType.Pipeline, "BatchAccountSubscription", "SUBSCRIPTION_ID"),
            RunParameter(RunParameterType.Pipeline, "BatchAccountResourceGroup", "RESOURCE_GROUP"),
            RunParameter(
                RunParameterType.Pipeline, "BatchURI", "https://batch-account-name.westeurope.batch.azure.com"
            ),
            RunParameter(RunParameterType.Pipeline, "ADFSubscription", "bd19dba4-89ad-4976-b862-848bf43a4340"),
            RunParameter(RunParameterType.Pipeline, "ADFResourceGroup", "adf-rg"),
            RunParameter(RunParameterType.Pipeline, "ADFName", "adf-name"),
        ],
    )

    # Assert
    activity = next(activities)
    assert activity.name == "Set UserAssignedIdentityReference"
    assert activity.type_properties["variableName"] == "UserAssignedIdentityReference"
    assert (
        activity.type_properties["value"].value
        == "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"  # noqa: E501
    )

    activity = next(activities)
    assert activity.name == "Set ManagerApplicationPackagePath"
    assert activity.type_properties["variableName"] == "ManagerApplicationPackagePath"
    assert activity.type_properties["value"].value == "$AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz"

    activity = next(activities)
    assert activity.name == "Set WorkloadApplicationPackagePath"
    assert activity.type_properties["variableName"] == "WorkloadApplicationPackagePath"
    assert (
        activity.type_properties["value"].value
        == "$AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz"
    )

    activity = next(activities)
    assert activity.name == "Set CommonEnvironmentSettings"
    assert activity.type_properties["variableName"] == "CommonEnvironmentSettings"
    # noqa: E501
    assert (
        activity.type_properties["value"].value
        == """[
    {
        "name": "WORKLOAD_APP_PACKAGE",
        "value": "test-application"
    },
    {
        "name": "WORKLOAD_APP_PACKAGE_VERSION",
        "value": "1.5.0"
    },
    {
        "name": "MANAGER_APP_PACKAGE",
        "value": "batchmanager"
    },
    {
        "name": "MANAGER_APP_PACKAGE_VERSION",
        "value": "2.0.0"
    },
    {
        "name": "BATCH_JOB_TIMEOUT",
        "value": "PT4H"
    },
    {
        "name": "WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME",
        "value": "batch-account-name"
    },
    {
        "name": "WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID",
        "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"
    },
    {
        "name": "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID",
        "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"
    }
    ]"""  # noqa: E501
    )

    activity = next(activities)
    assert activity.name == "Set JobContainerName"
    assert activity.type_properties["variableName"] == "JobContainerName"
    assert activity.type_properties["value"].value == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a"

    activity = next(activities)
    assert activity.name == "Set Job Container URL"
    assert activity.type_properties["variableName"] == "JobContainerURL"
    assert (
        activity.type_properties["value"].value
        == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a"
    )

    activity = next(activities)
    assert activity.name == "Create Job Storage Container"
    assert (
        activity.type_properties["relativeUrl"].value
        == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container"
    )
    assert activity.type_properties["method"] == "PUT"
    assert activity.type_properties["body"].value == "{}"

    activity = next(activities)
    assert activity.name == "Start Job"
    assert activity.type_properties["relativeUrl"] == "/jobs?api-version=2022-10-01.16.0"
    assert activity.type_properties["method"] == "POST"
    assert (
        activity.type_properties["body"].value
        == """{
    "id": "802100a5-ec79-4a52-be62-8d6109f3ff9a",
    "priority": 100,
    "constraints": {
        "maxWallClockTime":"PT4H",
        "maxTaskRetryCount": 0
    },
    "jobManagerTask": {
        "id": "Manager",
        "displayName": "Manager",
        "authenticationTokenSettings": {
            "access": [
                "job"
            ]
        },
        "commandLine": "/bin/bash -c \\"python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz && python3 -m test-application job --parameter1 dummy --parameter2 another-dummy\\"",
        "applicationPackageReferences": [
            {
                "applicationId": "batchmanager",
                "version": "2.0.0"
            },
            {
                "applicationId": "test-application",
                "version": "1.5.0"
            }
        ],
        "outputFiles": [
            {
                "destination": {
                    "container": {
                        "containerUrl": "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a",
                        "identityReference": {
                            "resourceId": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"
                        },
                        "path": "Manager/$TaskLog"
                    }
                },
                "filePattern": "../*.txt",
                "uploadOptions": {
                    "uploadCondition": "taskcompletion"
                }
            }
        ],
        "environmentSettings": [],
        "requiredSlots": 1,
        "killJobOnCompletion": false,
        "userIdentity": {
            "username": null,
            "autoUser": {
                "scope": "pool",
                "elevationLevel": "nonadmin"
            }
        },
        "runExclusive": true,
        "allowLowPriorityNode": true
    },
    "poolInfo": {
        "poolId": "batch-pool-id"
    },
    "onAllTasksComplete": "terminatejob",
    "onTaskFailure": "noaction",
    "usesTaskDependencies": true,
    "commonEnvironmentSettings": [{"name": "WORKLOAD_APP_PACKAGE", "value": "test-application"}, {"name": "WORKLOAD_APP_PACKAGE_VERSION", "value": "1.5.0"}, {"name": "MANAGER_APP_PACKAGE", "value": "batchmanager"}, {"name": "MANAGER_APP_PACKAGE_VERSION", "value": "2.0.0"}, {"name": "BATCH_JOB_TIMEOUT", "value": "PT4H"}, {"name": "WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME", "value": "batch-account-name"}, {"name": "WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID", "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"}, {"name": "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID", "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"}]}"""  # noqa: E501
    )

    activity = next(activities)
    assert activity.name == "Monitor Batch Job"
    assert activity.type_properties["pipeline"]["referenceName"] == "4e66b9d6-d1b9-4d2b-9b89-4101def23c9a"
    assert len(activity.type_properties["parameters"]) == 1
    assert activity.type_properties["parameters"]["JobId"].value == "802100a5-ec79-4a52-be62-8d6109f3ff9a"

    activity = next(activities)
    assert activity.name == "Copy Output Files"
    assert activity.type_properties["pipeline"]["referenceName"] == "4e66b9d6-d1b9-4d2b-9b89-4101def23c9a"
    assert len(activity.type_properties["parameters"]) == 5
    assert (
        activity.type_properties["parameters"]["JobContainerName"].value == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a"
    )
    assert activity.type_properties["parameters"]["TaskOutputFolderPrefix"].value == "TASKOUTPUT_"
    assert (
        activity.type_properties["parameters"]["OutputStorageAccountName"].value
        == "test-application-output-storage-account-name"
    )
    assert (
        activity.type_properties["parameters"]["OutputContainerName"].value == "test-application-output-container-name"
    )
    assert activity.type_properties["parameters"]["OutputFolderName"].value == "TEMP"

    activity = next(activities)
    assert activity.name == "Delete Job Storage Container"
    assert activity.type_properties["relativeUrl"].value == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container"
    assert activity.type_properties["method"] == "DELETE"
    assert "body" not in activity.type_properties

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
