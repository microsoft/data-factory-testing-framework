from typing import List

from data_factory_testing_framework.models.base.run_parameter import RunParameter


class RunState:
    def __init__(self, parameters: List[RunParameter]):
        self.parameters = parameters
