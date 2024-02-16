from data_factory_testing_framework.exceptions._user_error import UserError


class StateIterationItemNotSetError(UserError):
    def __init__(self) -> None:
        """Error raised when an iteration item is not set."""
        super().__init__("Iteration item not set.")
