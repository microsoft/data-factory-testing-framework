import inspect
import types
import typing
from typing import Optional

from data_factory_testing_framework import TestFrameworkType
from data_factory_testing_framework.models import Pipeline
from data_factory_testing_framework.models.activities import Activity
from data_factory_testing_framework.state import PipelineRunState, RunParameter

from tests.functional import utils


def test_test_framework_api() -> None:
    # Arrange
    from data_factory_testing_framework import TestFramework

    # Act
    public_attributes = [attribute for attribute in dir(TestFramework) if not attribute.startswith("_")]

    # Assert
    assert public_attributes == [
        "evaluate_activities",
        "evaluate_activity",
        "evaluate_pipeline",
        "get_pipeline_by_id",
        "get_pipeline_by_name",
        "should_evaluate_child_pipelines",
    ]


def test_test_framework_method_types() -> None:
    # Arrange
    from data_factory_testing_framework import TestFramework

    # Act
    method_types = {name: type(getattr(TestFramework, name)) for name in dir(TestFramework) if not name.startswith("_")}

    # Assert
    assert method_types == {
        "evaluate_activities": types.FunctionType,
        "evaluate_activity": types.FunctionType,
        "evaluate_pipeline": types.FunctionType,
        "get_pipeline_by_id": types.FunctionType,
        "get_pipeline_by_name": types.FunctionType,
        "should_evaluate_child_pipelines": property,
    }


def test_test_framework_method_properties() -> None:
    # Arrange
    from data_factory_testing_framework import TestFramework

    # Act
    properties = [method[0] for method in inspect.getmembers(TestFramework, predicate=utils.is_property)]

    # Assert
    assert properties == ["should_evaluate_child_pipelines"]
    assert TestFramework.should_evaluate_child_pipelines.fget.__annotations__ == {"return": bool}


def test_test_framework_method_signatures() -> None:
    # Arrange
    from data_factory_testing_framework import TestFramework

    methods = [method[0] for method in inspect.getmembers(TestFramework, predicate=utils.is_public_method)]

    # Act
    method_signatures = {name: inspect.signature(getattr(TestFramework, name)) for name in methods}

    # Assert
    assert method_signatures == {
        "__init__": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(
                    name="framework_type", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=TestFrameworkType
                ),
                inspect.Parameter(
                    name="root_folder_path",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=None,
                    annotation=Optional[str],
                ),
                inspect.Parameter(
                    name="should_evaluate_child_pipelines",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=False,
                    annotation=Optional[bool],
                ),
            ],
            return_annotation=None,
        ),
        "evaluate_activities": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(
                    name="activities", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=typing.List[Activity]
                ),
                inspect.Parameter(
                    name="state", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=PipelineRunState
                ),
            ],
            return_annotation=typing.Iterator[Activity],
        ),
        "evaluate_activity": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(name="activity", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Activity),
                inspect.Parameter(
                    name="state", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=PipelineRunState
                ),
            ],
            return_annotation=typing.Iterator[Activity],
        ),
        "evaluate_pipeline": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(name="pipeline", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Pipeline),
                inspect.Parameter(
                    name="parameters",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=typing.List[RunParameter],
                ),
            ],
            return_annotation=typing.Iterator[Activity],
        ),
        "get_pipeline_by_id": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(name="id_", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            ],
            return_annotation=Pipeline,
        ),
        "get_pipeline_by_name": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(name="name", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            ],
            return_annotation=Pipeline,
        ),
    }
