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
    env_settings = activity.type_properties["value"].value
    assert env_settings[0]["name"] == "WORKLOAD_APP_PACKAGE"
    assert env_settings[0]["value"] == "workload"
    assert env_settings[1]["name"] == "WORKLOAD_APP_PACKAGE_VERSION"
    assert env_settings[1]["value"] == "0.13.2"
    assert env_settings[2]["name"] == "MANAGER_APP_PACKAGE"
    assert env_settings[2]["value"] == "managerworkload"
    assert env_settings[3]["name"] == "MANAGER_APP_PACKAGE_VERSION"
    assert env_settings[3]["value"] == "0.13.2"
    assert env_settings[4]["name"] == "BATCH_JOB_TIMEOUT"
    assert env_settings[4]["value"] == "PT4H"
    assert env_settings[5]["name"] == "WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME"
    assert env_settings[5]["value"] == "batch-account-name"
    assert env_settings[6]["name"] == "WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID"
    assert (
        env_settings[6]["value"]
        == "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"
    )
    assert env_settings[7]["name"] == "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID"
    assert env_settings[7]["value"] == "workload-user-assigned-identity-client-id"


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

    body = activity.type_properties["body"].get_json_value()
    assert body["id"] == "8b6b545b-c583-4a06-adf7-19ff41370aba"
    assert body["priority"] == 100
    assert body["constraints"]["maxWallClockTime"] == "PT4H"
    assert body["constraints"]["maxTaskRetryCount"] == 0
    job_manager_task = body["jobManagerTask"]
    assert job_manager_task["id"] == "Manager"
    assert job_manager_task["displayName"] == "Manager"
    assert job_manager_task["authenticationTokenSettings"]["access"] == ["job"]
    assert (
        job_manager_task["commandLine"]
        == '/bin/bash -c "python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_managerworkload_0_13_2/managerworkload.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_workload_0_13_2/workload.tar.gz && python3 -m test-application-name job --parameter1 dummy --parameter2 another-dummy"'
    )
    application_package_references = job_manager_task["applicationPackageReferences"]
    assert application_package_references[0]["applicationId"] == "batchmanager"
    assert application_package_references[0]["version"] == "2.0.0"
    assert application_package_references[1]["applicationId"] == "test-application-name"
    assert application_package_references[1]["version"] == "1.5.0"
    assert (
        job_manager_task["outputFiles"][0]["destination"]["container"]["containerUrl"]
        == "https://batchstorage.blob.core.windows.net/job-8b6b545b-c583-4a06-adf7-19ff41370aba"
    )
    assert (
        job_manager_task["outputFiles"][0]["destination"]["container"]["identityReference"]["resourceId"]
        == "/subscriptions/batch-account-subscription/resourcegroups/batch-account-resource-group/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workload-user-assigned-identity-name"  # noqa: E501
    )
    assert job_manager_task["outputFiles"][0]["destination"]["container"]["path"] == "Manager/$TaskLog"
    assert job_manager_task["outputFiles"][0]["filePattern"] == "../*.txt"
    assert job_manager_task["outputFiles"][0]["uploadOptions"]["uploadCondition"] == "taskcompletion"
    assert job_manager_task["environmentSettings"] == []
    assert job_manager_task["requiredSlots"] == 1
    assert job_manager_task["killJobOnCompletion"] is False
    assert job_manager_task["userIdentity"]["username"] is None
    assert job_manager_task["userIdentity"]["autoUser"]["scope"] == "pool"
    assert job_manager_task["userIdentity"]["autoUser"]["elevationLevel"] == "nonadmin"
    assert job_manager_task["runExclusive"] is True
    assert job_manager_task["allowLowPriorityNode"] is True
    assert body["poolInfo"]["poolId"] == "test-application-batch-pool-id"
    assert body["onAllTasksComplete"] == "terminatejob"
    assert body["onTaskFailure"] == "noaction"
    assert body["usesTaskDependencies"] is True
    common_environment_settings = body["commonEnvironmentSettings"]
    assert common_environment_settings[0]["name"] == "COMMON_ENV_SETTING"
    assert common_environment_settings[0]["value"] == "dummy"
    assert common_environment_settings[1]["name"] == "STORAGE_ACCOUNT_NAME"
    assert common_environment_settings[1]["value"] == "teststorage"


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
