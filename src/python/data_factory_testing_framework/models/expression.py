from typing import List, TypeVar

from data_factory_testing_framework.functions.function_parser import parse_expression
from data_factory_testing_framework.generated.models import Expression
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


TResult = TypeVar("TResult")


class Expression[TResult]:

    evaluated: TResult = []

    def evaluate(self: Expression, state: PipelineRunState):
        return parse_expression(self.expression).evaluate(state)