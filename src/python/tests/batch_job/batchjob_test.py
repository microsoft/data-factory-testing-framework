from data_factory_testing_framework.generated.models import WebActivity, DependencyCondition, SetVariableActivity
from data_factory_testing_framework.models.base.parameter_type import ParameterType
from data_factory_testing_framework.models.base.run_parameter import RunParameter
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.models.test_framework import TestFramework


class TestBatchJob:

    def test_batch_job_pipeline(self):
        # Arrange
        test_framework = TestFramework("pipelines")
        pipeline = test_framework.repository.get_pipeline_by_name("batch_job")
        state = PipelineRunState(parameters=[
            RunParameter(ParameterType.Pipeline, "BatchPoolId", "batch-pool-id"),
            RunParameter(ParameterType.Pipeline, "WorkloadApplicationPackageName", "test-application"),
            RunParameter(ParameterType.Pipeline, "WorkloadApplicationPackageVersion", "1.5.0"),
            RunParameter(ParameterType.Pipeline, "ManagerApplicationPackageName", "batchmanager"),
            RunParameter(ParameterType.Pipeline, "ManagerApplicationPackageVersion", "2.0.0"),
            RunParameter(ParameterType.Pipeline, "ManagerTaskParameters", "--parameter1 dummy --parameter2 another-dummy"),
            RunParameter(ParameterType.Pipeline, "JobId", "802100a5-ec79-4a52-be62-8d6109f3ff9a"),
            RunParameter(ParameterType.Pipeline, "TaskOutputFolderPrefix", "TASKOUTPUT_"),
            RunParameter(ParameterType.Pipeline, "WorkloadUserAssignedIdentityName", "test-application-identity-name"),
            RunParameter(ParameterType.Pipeline, "WorkloadUserAssignedIdentityClientId", "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"),
            RunParameter(ParameterType.Pipeline, "JobAdditionalEnvironmentSettings", "[]"),
            RunParameter(ParameterType.Pipeline, "OutputStorageAccountName", "test-application-output-storage-account-name"),
            RunParameter(ParameterType.Pipeline, "OutputContainerName", "test-application-output-container-name"),
            RunParameter(ParameterType.Pipeline, "OutputFolderName", "TEMP"),
            RunParameter(ParameterType.Pipeline, "BatchJobTimeout", "PT4H"),
            RunParameter(ParameterType.Global, "BatchStorageAccountName", "batch-account-name"),
            RunParameter(ParameterType.Global, "BatchAccountSubscription", "SUBSCRIPTION_ID"),
            RunParameter(ParameterType.Global, "BatchAccountResourceGroup", "RESOURCE_GROUP"),
            RunParameter(ParameterType.Global, "BatchURI", "https://batch-account-name.westeurope.batch.azure.com"),
            RunParameter(ParameterType.Global, "ADFSubscription", "bd19dba4-89ad-4976-b862-848bf43a4340"),
            RunParameter(ParameterType.Global, "ADFResourceGroup", "adf-rg"),
            RunParameter(ParameterType.Global, "ADFName", "adf-name"),
        ])

        # Act
        activities = test_framework.evaluate_pipeline(pipeline, state)

        # Assert
        activity: SetVariableActivity = next(activities)
        assert activity.name == "Set UserAssignedIdentityReference"
        assert activity.variable_name == "UserAssignedIdentityReference"
        # assert activity.value.value == "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"

        activity = next(activities)
        assert activity.name == "Set ManagerApplicationPackagePath"
        assert activity.variable_name == "ManagerApplicationPackagePath"
        # assert activity.value == "$AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz"

        activity = next(activities)
        assert activity.name == "Set WorkloadApplicationPackagePath"
        assert activity.variable_name == "WorkloadApplicationPackagePath"
        # assert activity.value == "$AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz"

        activity = next(activities)
        assert activity.name == "Set CommonEnvironmentSettings"
        assert activity.variable_name == "CommonEnvironmentSettings"
        # assert activity.value == """
        # [
        #     {
        #         "name": "WORKLOAD_APP_PACKAGE",
        #         "value": "test-application"
        #     },
        #     {
        #         "name": "WORKLOAD_APP_PACKAGE_VERSION",
        #         "value": "1.5.0"
        #     },
        #     {
        #         "name": "MANAGER_APP_PACKAGE",
        #         "value": "batchmanager"
        #     },
        #     {
        #         "name": "MANAGER_APP_PACKAGE_VERSION",
        #         "value": "2.0.0"
        #     },
        #     {
        #         "name": "BATCH_JOB_TIMEOUT",
        #         "value": "PT4H"
        #     },
        #     {
        #         "name": "WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME",
        #         "value": "batch-account-name"
        #     },
        #     {
        #         "name": "WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID",
        #         "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"
        #     },
        #     {
        #         "name": "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID",
        #         "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"
        #     }
        # ]
        # """

        activity = next(activities)
        assert activity.name == "Set JobContainerName"
        assert activity.variable_name == "JobContainerName"
        #assert activity.value == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a"

        activity = next(activities)
        assert activity.name == "Set Job Container URL"
        assert activity.variable_name == "JobContainerURL"
        #assert activity.value == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a"

        activity = next(activities)
        assert activity.name == "Create Job Storage Container"
        #assert activity.url == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container"
        assert activity.method == "PUT"
        #assert activity.body == "{}"

        activity = next(activities)
        assert activity.name == "Start Job"
        #assert activity.uri == "https://batch-account-name.westeurope.batch.azure.com/jobs?api-version=2022-10-01.16.0"
        assert activity.method == "POST"
        # assert activity.body == """
        # {
        #     "id": "802100a5-ec79-4a52-be62-8d6109f3ff9a",
        #     "priority": 100,
        #     "constraints": {
        #         "maxWallClockTime": "PT4H",
        #         "maxTaskRetryCount": 0
        #     },
        #     "jobManagerTask": {
        #         "id": "Manager",
        #         "displayName": "Manager",
        #         "authenticationTokenSettings": {
        #             "access": [
        #                 "job"
        #             ]
        #         },
        #         "commandLine": "/bin/bash -c \"python3 -m ensurepip --upgrade && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_batchmanager_2_0_0/batchmanager.tar.gz && python3 -m pip install --user $AZ_BATCH_APP_PACKAGE_test-application_1_5_0/test-application.tar.gz && python3 -m test-application job --parameter1 dummy --parameter2 another-dummy\"",
        #         "applicationPackageReferences": [
        #             {
        #                 "applicationId": "batchmanager",
        #                 "version": "2.0.0"
        #             },
        #             {
        #                 "applicationId": "test-application",
        #                 "version": "1.5.0"
        #             }
        #         ],
        #         "outputFiles": [
        #             {
        #                 "destination": {
        #                     "container": {
        #                         "containerUrl": "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a",
        #                         "identityReference": {
        #                             "resourceId": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"
        #                         },
        #                         "path": "Manager/$TaskLog"
        #                     }
        #                 },
        #                 "filePattern": "../*.txt",
        #                 "uploadOptions": {
        #                     "uploadCondition": "taskcompletion"
        #                 }
        #             }
        #         ],
        #         "environmentSettings": [],
        #         "requiredSlots": 1,
        #         "killJobOnCompletion": false,
        #         "userIdentity": {
        #             "username": null,
        #             "autoUser": {
        #                 "scope": "pool",
        #                 "elevationLevel": "nonadmin"
        #             }
        #         },
        #         "runExclusive": true,
        #         "allowLowPriorityNode": true
        #     },
        #     "poolInfo": {
        #         "poolId": "batch-pool-id"
        #     },
        #     "onAllTasksComplete": "terminatejob",
        #     "onTaskFailure": "noaction",
        #     "usesTaskDependencies": true,
        #     "commonEnvironmentSettings": [{"name": "WORKLOAD_APP_PACKAGE", "value": "test-application"}, {"name": "WORKLOAD_APP_PACKAGE_VERSION", "value": "1.5.0"}, {"name": "MANAGER_APP_PACKAGE", "value": "batchmanager"}, {"name": "MANAGER_APP_PACKAGE_VERSION", "value": "2.0.0"}, {"name": "BATCH_JOB_TIMEOUT", "value": "PT4H"}, {"name": "WORKLOAD_AUTO_STORAGE_ACCOUNT_NAME", "value": "batch-account-name"}, {"name": "WORKLOAD_USER_ASSIGNED_IDENTITY_RESOURCE_ID", "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"}, {"name": "WORKLOAD_USER_ASSIGNED_IDENTITY_CLIENT_ID", "value": "/subscriptions/SUBSCRIPTION_ID/resourcegroups/RESOURCE_GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/test-application-identity-name"}]
        # }"""

        activity = next(activities)
        assert activity.name == "Monitor Batch Job"
        assert activity.pipeline.reference_name == "monitor_batch_job"
        assert len(activity.parameters) == 1
        # assert activity.parameters["JobId"] == "802100a5-ec79-4a52-be62-8d6109f3ff9a"

        activity = next(activities)
        assert activity.name == "Copy Output Files"
        assert activity.pipeline.reference_name == "copy_output_files"
        assert len(activity.parameters) == 5
        # assert activity.parameters["JobContainerName"] == "job-802100a5-ec79-4a52-be62-8d6109f3ff9a"
        # assert activity.parameters["TaskOutputFolderPrefix"] == "TASKOUTPUT_"
        # assert activity.parameters["OutputStorageAccountName"] == "test-application-output-storage-account-name"
        # assert activity.parameters["OutputContainerName"] == "test-application-output-container-name"
        # assert activity.parameters["OutputFolderName"] == "TEMP"

        activity = next(activities)
        assert activity.name == "Delete Job Storage Container"
        # assert activity.uri == "https://batch-account-name.blob.core.windows.net/job-802100a5-ec79-4a52-be62-8d6109f3ff9a?restype=container"
        assert activity.method == "DELETE"
        # assert activity.body is None

        # Assert that there are no more activities
        try:
            next(activities)
            assert False  # This line should not be reached, an exception should be raised
        except StopIteration:
            pass


