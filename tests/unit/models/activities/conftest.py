import pytest
from data_factory_testing_framework.models._pipeline import Pipeline
from data_factory_testing_framework.state import RunParameter, RunParameterType


@pytest.fixture
def pipeline() -> Pipeline:
    """Fixture to create a sample pipeline."""
    return Pipeline(
        pipeline_id="sample_pipeline",
        name="SamplePipeline",
        activities=[],
        parameters=[
            RunParameter(name="param1", value="default_value", parameter_type=RunParameterType.Pipeline),
        ],
    )