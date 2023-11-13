from data_factory_testing_framework.generated.models import ControlActivity, SetVariableActivity
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class SetVariableActivity:
    def evaluate(self: SetVariableActivity, state: PipelineRunState) -> SetVariableActivity:
        super(ControlActivity, self).evaluate(state)

        if self.variable_name == "pipelineReturnValue":
            return self

        state.set_variable(self.variable_name, self.value.evaluate(state))

        return self
