import re

from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


def find_and_replace_iteration_item(expression: str, state: PipelineRunState):
    pattern = fr'(@?{{?item\(\)\}}?)'
    matches = re.finditer(pattern, expression, re.MULTILINE)
    for match in matches:
        expression = expression.replace(match.group(0), state.iteration_item)

    return expression
