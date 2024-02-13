from typing import Union

from data_factory_testing_framework.exceptions.expression_evaluation_error import ExpressionEvaluationError


class ExpressionEvaluationInvalidNumberOfChildrenError(ExpressionEvaluationError):
    """Expression evaluation invalid number of children error."""

    def __init__(self, required: int, actual: int) -> None:
        """Initialize expression evaluation invalid number of children error."""
        super().__init__(f"Invalid number of children. Required: {required}, Actual: {actual}")


class ExpressionEvaluationInvalidChildTypeError(ExpressionEvaluationError):
    """Expression evaluation invalid child type error."""

    def __init__(self, child_index: int, expected_types: Union[tuple[type], type], actual_type: type) -> None:
        """Initialize expression evaluation invalid child type error."""
        super().__init__(
            f"Invalid child type at index {child_index}. Expected: {expected_types}, Actual: {actual_type}"
        )
