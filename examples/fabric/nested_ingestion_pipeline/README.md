# Nested pipelines

The following example, exemplifies the utilization of nested pipelines including control activities like ForEach and If.

![Nested Pipelines](pl_main_pipeline.png)

The main pipeline is composed of 2 top activities:

- a lookup activity named "Read Configuration File
- a ForEach activity names "ForEach"

Within the ForEach activity, there is a nested If activity called "If New Or Updated" and if this activity evaluates to True, a Invoke Pipeline activity named "Invoke Ingestion Pipeline" is triggered.

The Ingestion pipeline is composed also by two activities:

- a Copy activity named "Copy NYCData to ADLS" that copies from the Web to an ADLS Gen2 storage,
- a Copy activity named "CopyNYCData to Lakehouse" that copies from the ADLS Gen2 storage to the Lakehouse.

![Ingestion Pipeline](pl_ingestion_pipeline.png)

## Testing the pl_main activities

The file that contains the individual activity tests for the pl_main_pipeline is located [here](./fabric/tests/test_pl_main_activity.py) and it contains three individual activity tests:

- test_activity_read_configuration_file, which is responsible to test if the json configuration file is correctly located and defined.
- test_activity_if, responsible to check id the if condition expression is well formed in order to decide wheather or not new or updated data should be ingested.
- test_activity_invoke_pipeline, responsible to check if the nested pipeline is correctly invoked.

## Testing the pl_ingestion activities

The file that contains the individual activity tests for the pl_ingestion_pipeline is located [here](./fabric/tests/test_pl_ingestion_activity.py) and it contains two individual activity test:

- test_copy_nyc_data_to_adls2, this test is responsible to test if the source path is correct and id the target path where the data should land in the datalake is well formed and within the correct stablished partition norms.
- test_copy_nyc_data_to_lakehouse, similar to the previous one but the previous target is now the source and the current target is the Fabric Lakehouse.

## Testing the pl_main pipeline with should_evaluate_child_pipelines=False

When testing a pipeline and instantiating the framework, there is a flag called: should_evaluate_child_pipelines. When setting this flag to False, it means that the test is just being done on the main pipeline and the child pipeline will not be loaded for evaluation. Check the code below:

```python
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path = os.path.join(Path(__file__).parent.parent),
        should_evaluate_child_pipelines=False
```

You can find the entire code  [here](./fabric/tests/test_pl_main_pipeline_child_flag_false.py).

In this specific case you can test for the number of activities within the pipeline and respective types for example. Furthermore, you can do similar tests to the ones were done on the individual activity tests.

For this particular pipeline, we will have two activities to evaluate:

- read_configuration_file_activity = next(activities)
- invoke_ingestion_pipeline_activity =  next(activities)

For the control activities, If and ForEach in this specific pipeline, the framework does the evaluation in the background so they won't be available when running the next(activities) function.

## Testing the pl_main pipeline with should_evaluate_child_pipelines=True

Setting the should_evaluate_child_pipelines flag to True, it means that the test is being done on the main pipeline jointly with the child pipeline. Check the code below:
below:

```python
def test_framework(request: pytest.FixtureRequest) -> TestFramework:
    return TestFramework(
        framework_type=TestFrameworkType.Fabric,
        root_folder_path = os.path.join(Path(__file__).parent.parent),
        should_evaluate_child_pipelines=True
```

You can find the entire code  [here](./fabric/tests/test_pl_main_pipeline_child_flag_true.py).

In this specific case you can test for the number of activities within the pipeline and respective types for example. Furthermore, you can do similar tests to the ones were done on the individual activity tests.

For this particular pipeline, we will have three activities to evaluate, the first one belongs to the pl_main pipeline and the second and third ones belong to the pl_ingestion pipeline:

- read_configuration_file_activity = next(activities)
- copy_nyc_data_to_adls_pipeline_activity =  next(activities)
- copy_nyc_data_to_lakehouse_pipeline_activity =  next(activities)

## Additional Notes

Be aware that when using the previous json files on your environment, you might need to adjust the connection IDs, as for example:

```json
              "externalReferences": {
                "connection": "a97f9477-e2b0-4a61-bc57-081255466130"
              }
```

In this specific example you need to create three connections in the json definition files:

- the connection to the Web where the Taxi Data is being pulled from
- connection to the ADLSGen2 storage account
- connection to the Fabric Lakehouse
