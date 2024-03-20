
from data_factory_testing_framework.state import PipelineRunState
from data_factory_testing_framework._pythonnet.logic_apps_expression_evaluator import LogicAppsExpressionEvaluator

if __name__ == "__main__":
    state = PipelineRunState(
        activity_results=[],
        iteration_item="tst",
        parameters=[],
        variables=[],
    )

    expression = "@pipeline().p1"
    result = LogicAppsExpressionEvaluator.evaluate(expression, state)