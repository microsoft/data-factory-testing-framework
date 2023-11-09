from typing import List

from data_factory_testing_framework.generated.models import Expression
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class Expression:

    evaluated_items: List[str] = []

    @staticmethod
    def patch_generated_models(models):
        models.Expression.evaluate = Expression.evaluate

    def evaluate(self: Expression, state: PipelineRunState):
        self.evaluated_items = [
            "item1",
            "item2",
            "item3"
        ]