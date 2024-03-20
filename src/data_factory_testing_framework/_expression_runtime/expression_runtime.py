from data_factory_testing_framework._expression_runtime.data_factory_expression.expression_transformer import (
    ExpressionTransformer as DataFactoryExpressionTransformer,
)
from data_factory_testing_framework._pythonnet.logic_apps_expression_evaluator import LogicAppsExpressionEvaluator
from data_factory_testing_framework.state import PipelineRunState


class ExpressionRuntime:
    def __init__(self):
        self.data_factory_expression_transformer = DataFactoryExpressionTransformer()
        self.logic_apps_expression_evaluator = LogicAppsExpressionEvaluator()

    def evaluate(self, expression: str, state: PipelineRunState) -> str:
        logic_apps_expression = self.data_factory_expression_transformer.transform_to_logic_apps_expression(
            expression, state
        )
        return self.logic_apps_expression_evaluator.evaluate(logic_apps_expression, state)
