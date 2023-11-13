class StateIterationItemNotSet(Exception):
    def __init__(self) -> None:
        super().__init__("Iteration item not set.")
