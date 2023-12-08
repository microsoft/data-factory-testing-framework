# flake8: noqa: E501
import pytest
from data_factory_testing_framework.models.pipeline import Pipeline
from data_factory_testing_framework.state import (
    PipelineRunState,
    PipelineRunVariable,
    RunParameter,
    RunParameterType,
)
from data_factory_testing_framework.test_framework import TestFramework, TestFrameworkType


@pytest.fixture
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.DataFactory,
        root_folder_path=request.fspath.dirname,
    )


@pytest.fixture
def pipeline(test_framework: TestFramework) -> Pipeline:
    return test_framework.repository.get_pipeline_by_name("batch_job")


def test_set_job_container_url(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Set Job Container URL")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="JobContainerURL"),
            PipelineRunVariable(name="JobContainerName", default_value="job-8b6b545b-c583-4a06-adf7-19ff41370aba"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Global, "BatchStorageAccountName", "batch-account-name"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    updated_variable = state.get_variable_by_name("JobContainerURL")
    expected_url = "https://batch-account-name.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba"
    assert activity.type_properties["value"].value == expected_url
    assert updated_variable.value == expected_url


def test_set_user_assigned_identity_reference(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Set UserAssignedIdentityReference")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="UserAssignedIdentityReference"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Global, "BatchAccountSubscription", "batch-account-subscription"),
            RunParameter[str](RunParameterType.Global, "BatchAccountResourceGroup", "batch-account-resource-group"),
            RunParameter[str](
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityName",
                "workload-user-assigned-identity-name",
            ),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    updated_variable = state.get_variable_by_name("UserAssignedIdentityReference")
    expected_reference = "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"
    assert activity.type_properties["value"].value == expected_reference
    assert updated_variable.value == expected_reference


def test_set_manager_application_package_path(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Set ManagerApplicationPackagePath")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="ManagerApplicationPackagePath"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Pipeline, "ManagerApplicationPackageName", "managerworkload"),
            RunParameter[str](RunParameterType.Pipeline, "ManagerApplicationPackageVersion", "0.13.2"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    updated_variable = state.get_variable_by_name("ManagerApplicationPackagePath")
    expected_path = "$AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz"
    assert activity.type_properties["value"].value == expected_path
    assert updated_variable.value == expected_path


def test_set_workload_application_package_path(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Set WorkloadApplicationPackagePath")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="WorkloadApplicationPackagePath"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Pipeline, "WorkloadApplicationPackageName", "workload"),
            RunParameter[str](RunParameterType.Pipeline, "WorkloadApplicationPackageVersion", "0.13.2"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    updated_variable = state.get_variable_by_name("WorkloadApplicationPackagePath")
    expected_path = "$AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz"
    assert activity.type_properties["value"].value == expected_path
    assert updated_variable.value == expected_path


def test_set_common_environment_settings(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Set CommonEnvironmentSettings")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="CommonEnvironmentSettings"),
            PipelineRunVariable(
                name="UserAssignedIdentityReference",
                default_value="/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name",
            ),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Pipeline, "WorkloadApplicationPackageName", "workload"),
            RunParameter[str](RunParameterType.Pipeline, "WorkloadApplicationPackageVersion", "0.13.2"),
            RunParameter[str](RunParameterType.Pipeline, "ManagerApplicationPackageName", "managerworkload"),
            RunParameter[str](RunParameterType.Pipeline, "ManagerApplicationPackageVersion", "0.13.2"),
            RunParameter[str](RunParameterType.Pipeline, "BatchJobTimeout", "PT4H"),
            RunParameter[str](RunParameterType.Global, "BatchStorageAccountName", "batch-account-name"),
            RunParameter[str](
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityName",
                "workload-user-assigned-identity-name",
            ),
            RunParameter[str](
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityClientId",
                "workload-user-assigned-identity-client-id",
            ),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    expected_settings = """[
    {
        "name": "WORKLOAD_APP_PACKAGE",
        "value": "workload"
    },
    {
        "name": "WORKLOAD_APP_PACKAGE_VERSION",
        "value": "0.13.2"
    },
    {
        "name": "MANAGER_APP_PACKAGE",
        "value": "managerworkload"
    },
    {
        "name": "MANAGER_APP_PACKAGE_VERSION",
        "value": "0.13.2"
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
        "value": "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"
    },
    {
        "name": "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID",
        "value": "workload-user-assigned-identity-client-id"
    }
    ]"""
    assert activity.type_properties["value"].value == expected_settings
    assert state.get_variable_by_name("CommonEnvironmentSettings").value == expected_settings


def test_create_job_storage_container(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Create Job Storage Container")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(
                name="JobContainerURL",
                default_value="https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba",
            ),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "Create Job Storage Container"
    assert (
        activity.type_properties["url"].value
        == "https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba?restype=container"
    )
    assert activity.type_properties["method"] == "PUT"
    assert activity.type_properties["body"].value == "{}"


def test_set_job_container_name(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Set JobContainerName")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="JobContainerName"),
        ],
        parameters=[RunParameter[str](RunParameterType.Pipeline, "JobId", "8b6b545b-c583-4a06-adf7-19ff41370aba")],
    )

    # Act
    activity.evaluate(state)

    # Assert
    job_container_name_variable = state.get_variable_by_name("JobContainerName")
    assert activity.type_properties["value"].value == "job-8b6b545b-c583-4a06-adf7-19ff41370aba"
    assert job_container_name_variable.value == "job-8b6b545b-c583-4a06-adf7-19ff41370aba"


def test_start_job_pipeline(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Start Job")
    state = PipelineRunState(
        parameters=[
            RunParameter[str](
                RunParameterType.Global,
                "BatchURI",
                "https://batch-account-name.westeurope.batch.azure.com",
            ),
            RunParameter[str](RunParameterType.Global, "BatchStorageAccountName", "batchstorage"),
            RunParameter[str](RunParameterType.Global, "ADFSubscription", "d9153e28-dd4e-446c-91e4-0b1331b523f1"),
            RunParameter[str](RunParameterType.Global, "ADFResourceGroup", "adf-rg"),
            RunParameter[str](RunParameterType.Global, "ADFName", "adf-name"),
            RunParameter[str](RunParameterType.Pipeline, "JobId", "8b6b545b-c583-4a06-adf7-19ff41370aba"),
            RunParameter[str](RunParameterType.Pipeline, "BatchJobTimeout", "PT4H"),
            RunParameter[str](RunParameterType.Pipeline, "BatchPoolId", "test-application-batch-pool-id"),
            RunParameter[str](RunParameterType.Pipeline, "WorkloadApplicationPackageName", "test-application-name"),
            RunParameter[str](RunParameterType.Pipeline, "WorkloadApplicationPackageVersion", "1.5.0"),
            RunParameter[str](RunParameterType.Pipeline, "ManagerApplicationPackageName", "batchmanager"),
            RunParameter[str](RunParameterType.Pipeline, "ManagerApplicationPackageVersion", "2.0.0"),
            RunParameter[str](
                RunParameterType.Pipeline,
                "ManagerTaskParameters",
                "--parameter1 dummy --parameter2 another-dummy",
            ),
            RunParameter[str](
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityName",
                "test-application-batch-pool-id",
            ),
            RunParameter[str](
                RunParameterType.Pipeline,
                "WorkloadUserAssignedIdentityClientId",
                "test-application-identity-client-id",
            ),
            RunParameter[str](
                RunParameterType.Pipeline,
                "JobAdditionalEnvironmentSettings",
                '[{"name": "STORAGE_ACCOUNT_NAME", "value": "teststorage"}]',
            ),
        ],
        variables=[
            PipelineRunVariable(
                name="JobContainerURL",
                default_value="https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba",
            ),
            PipelineRunVariable(
                name="UserAssignedIdentityReference",
                default_value="/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name",
            ),
            PipelineRunVariable(
                name="ManagerApplicationPackagePath",
                default_value="$AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz",
            ),
            PipelineRunVariable(
                name="WorkloadApplicationPackagePath",
                default_value="$AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz",
            ),
            PipelineRunVariable(
                name="CommonEnvironmentSettings", default_value='[{"name":"COMMON_ENV_SETTING","value":"dummy"}]'
            ),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert "Start Job" == activity.name
    assert (
        "https://batch-account-name.westeurope.batch.azure.com/jobs?api-version=2022-10-01.16.0"
        == activity.type_properties["url"].value
    )
    assert "POST" == activity.type_properties["method"]

    expected_body = """{
    "id": "8b6b545b-c583-4a06-adf7-19ff41370aba",
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
        "commandLine": "/bin/bash -c \\"python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz && python3 -m test-application-name job --parameter1 dummy --parameter2 another-dummy\\"",
        "applicationPackageReferences": [
            {
                "applicationId": "batchmanager",
                "version": "2.0.0"
            },
            {
                "applicationId": "test-application-name",
                "version": "1.5.0"
            }
        ],
        "outputFiles": [
            {
                "destination": {
                    "container": {
                        "containerUrl": "https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba",
                        "identityReference": {
                            "resourceId": "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"
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
        "poolId": "test-application-batch-pool-id"
    },
    "onAllTasksComplete": "terminatejob",
    "onTaskFailure": "noaction",
    "usesTaskDependencies": true,
    "commonEnvironmentSettings": [{"name": "COMMON_ENV_SETTING", "value": "dummy"}, {"name": "STORAGE_ACCOUNT_NAME", "value": "teststorage"}]}"""

    assert activity.type_properties["body"].value == expected_body


def test_monitor_job(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Monitor Batch Job")
    state = PipelineRunState(
        parameters=[
            RunParameter[str](RunParameterType.Pipeline, "JobId", "8b6b545b-c583-4a06-adf7-19ff41370aba"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "Monitor Batch Job"
    assert activity.type_properties["pipeline"]["referenceName"] == "monitor_batch_job"
    assert len(activity.type_properties["parameters"]) == 1
    assert activity.type_properties["parameters"]["JobId"].value == "8b6b545b-c583-4a06-adf7-19ff41370aba"


def test_copy_output_files(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Copy Output Files")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="JobContainerName", default_value="job-8b6b545b-c583-4a06-adf7-19ff41370aba"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Pipeline, "TaskOutputFolderPrefix", "TASKOUTPUT_"),
            RunParameter[str](RunParameterType.Pipeline, "OutputStorageAccountName", "teststorage"),
            RunParameter[str](
                RunParameterType.Pipeline,
                "OutputContainerName",
                "test-application-output-container-name",
            ),
            RunParameter[str](RunParameterType.Pipeline, "OutputFolderName", "output"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "Copy Output Files"
    assert activity.type_properties["pipeline"]["referenceName"] == "copy_output_files"
    assert len(activity.type_properties["parameters"]) == 5
    assert (
        activity.type_properties["parameters"]["JobContainerName"].value == "job-8b6b545b-c583-4a06-adf7-19ff41370aba"
    )
    assert activity.type_properties["parameters"]["TaskOutputFolderPrefix"].value == "TASKOUTPUT_"
    assert activity.type_properties["parameters"]["OutputStorageAccountName"].value == "teststorage"
    assert (
        activity.type_properties["parameters"]["OutputContainerName"].value == "test-application-output-container-name"
    )
    assert activity.type_properties["parameters"]["OutputFolderName"].value == "output"


def test_delete_job_storage_container(test_framework: TestFramework, pipeline: Pipeline) -> None:
    # Arrange
    activity = pipeline.get_activity_by_name("Delete Job Storage Container")
    state = PipelineRunState(
        variables=[
            PipelineRunVariable(name="JobContainerName", default_value="job-8b6b545b-c583-4a06-adf7-19ff41370aba"),
        ],
        parameters=[
            RunParameter[str](RunParameterType.Global, "BatchStorageAccountName", "batchstorage"),
        ],
    )

    # Act
    activity.evaluate(state)

    # Assert
    assert activity.name == "Delete Job Storage Container"
    assert (
        activity.type_properties["url"].value
        == "https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba?restype=container"
    )
    assert activity.type_properties["method"] == "DELETE"
