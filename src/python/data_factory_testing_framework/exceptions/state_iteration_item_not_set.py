class StateIterationItemNotSet(Exception):
    def __init__(self):
        super().__init__("Iteration item not set.")
