from typing import Type

from data_factory_testing_framework.exceptions._user_error import UserError


class ControlActivityExpressionEvaluatedNotToExpectedTypeError(UserError):
    """ControlActivityExpressionEvaluatedNotToExpectedType.

    This exception is raised when a ControlActivities iteration expression is not evaluating to the expected type.
    This might be due incorrect expression or incorrectly registering activity results (e.g. registering a dictionary instead of expected list)
    """

    def __init__(self, activity_name: str, expected_type: Type) -> None:
        super().__init__(
            f"Iteration expression of Activity: '{activity_name}' does not evaluate to the expected type: '{expected_type.__name__}'."
        )
