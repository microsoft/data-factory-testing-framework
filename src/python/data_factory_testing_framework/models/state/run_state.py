from typing import List, Optional

from data_factory_testing_framework.models.base.run_parameter import RunParameter


class RunState:
    def __init__(self, parameters: Optional[List[RunParameter]] = None):
        if parameters is None:
            parameters = []

        self.parameters = parameters
