class StateIterationItemNotSetError(Exception):
    def __init__(self) -> None:
        """Error raised when an iteration item is not set."""
        super().__init__("Iteration item not set.")
