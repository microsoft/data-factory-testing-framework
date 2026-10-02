from typing import TYPE_CHECKING, Dict, List, Optional, Union
from typing import Any as TypingAny

from data_factory_testing_framework.mock_context import MockContext

if TYPE_CHECKING:
    from data_factory_testing_framework.models._pipeline import Pipeline
    from data_factory_testing_framework.models.activities._activity import Activity


class _AnyMarker(object):
    """Marker class to indicate that a mock applies to any scope level."""

    pass


Any = _AnyMarker()  # Marker for any scope level, used in Scope class


class Scope:
    """Defines where a mock should be applied.

    A scope can be defined at the pipeline, activity, or property level.
    Use the `Any` constant to indicate a mock applies to all instances at that level.
    """


    def __init__(
        self,
        pipeline: Union[str, "Pipeline", _AnyMarker] = Any,
        activity: Union[str, "Activity", _AnyMarker] = Any,
        type_property: Union[str, _AnyMarker] = Any,
    ) -> None:
        """Initialize a Scope object."""
        self.pipeline = pipeline
        self.activity = activity
        self.type_property = type_property

    def is_in_scope(
        self, mock_context: MockContext
    ) -> bool:
        """Check if the mock is in scope based on the provided context."""
        pipeline_match = self.pipeline == mock_context.pipeline or (
            isinstance(self.pipeline, str) and self.pipeline == mock_context.pipeline.name
        ) or self.pipeline == Any

        activity_match = (
            self.activity == mock_context.activity or
            (isinstance(self.activity, str) and self.activity == mock_context.activity.name) or
            self.activity == Any
        )

        type_property_match = (
            self.type_property == mock_context.property_path or
            (isinstance(self.type_property, str) and self.type_property == mock_context.property_path) or
            self.type_property == Any
        )
        return pipeline_match and activity_match and type_property_match


class Mock:
    """Base class for all mock implementations."""

    def __init__(self, scope: Optional[Scope] = None) -> None:
        """Initialize a mock with an optional scope."""
        self.scope = scope or Scope()


class ExpressionMock(Mock):
    """Mocks an expression function in Data Factory."""

    def __init__(
        self,
        function_name: str,
        mock_result: Union[str, int, float, bool, List[TypingAny], Dict[str, TypingAny]],
        scope: Optional[Scope] = None,
    ) -> None:
        """Initialize an ExpressionMock with a function name, mock result, and optional scope."""
        self.function_name = function_name
        self.mock_result = mock_result
        super().__init__(scope)
