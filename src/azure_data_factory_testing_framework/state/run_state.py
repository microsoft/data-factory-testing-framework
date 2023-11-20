from typing import List, Optional

from azure_data_factory_testing_framework.state.run_parameter import RunParameter


class RunState:
    def __init__(self, parameters: Optional[List[RunParameter]] = None) -> None:
        """Represents the RunState for non-pipeline runs, like LinkedServices, Datasets and Triggers.

        Args:
            parameters: The global and regular parameters to be used for evaluating expressions.
        """
        if parameters is None:
            parameters = []

        self.parameters = parameters
