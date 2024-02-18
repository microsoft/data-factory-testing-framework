import inspect
from typing import List, Optional

from data_factory_testing_framework.state import RunParameter

from tests.functional import utils


def test_run_state_api() -> None:
    # Arrange
    from data_factory_testing_framework.state import RunState

    # Act
    public_attributes = [attribute for attribute in dir(RunState) if not attribute.startswith("_")]

    # Assert
    assert public_attributes == []


def test_run_state_method_signatures() -> None:
    # Arrange
    from data_factory_testing_framework.state import RunState

    methods = [method[0] for method in inspect.getmembers(RunState, predicate=utils.is_public_method)]

    # Act
    method_signatures = {name: inspect.signature(getattr(RunState, name)) for name in methods}

    # Assert
    assert method_signatures == {
        "__init__": inspect.Signature(
            parameters=[
                inspect.Parameter(name="self", kind=inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter(
                    name="parameters",
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=None,
                    annotation=Optional[List[RunParameter]],
                ),
            ],
            return_annotation=None,
        ),
    }
