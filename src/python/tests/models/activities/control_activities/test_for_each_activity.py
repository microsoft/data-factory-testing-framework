from data_factory_testing_framework.generated.models import ForEachActivity, Expression, ExpressionType, \
    SetVariableActivity, DataFactoryElement
from data_factory_testing_framework.models.base.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.models.test_framework import TestFramework


class TestForEachActivity:

    def test_when_evaluate_child_activities_then_should_return_the_activity_with_item_expression_evaluated(self):
        # Arrange
        test_framework = TestFramework()
        for_each_activity = ForEachActivity(name="ForEachActivity",
                                            items=Expression(type=ExpressionType.EXPRESSION,
                                                             value="@split('a,b,c', ',')"),
                                            activities=[
                                                SetVariableActivity(name="setVariable", variable_name="variable",
                                                                    value=DataFactoryElement[str]("item()"),
                                                                    depends_on=[])
                                            ],
                                            depends_on=[])
        state = PipelineRunState()
        state.variables.append(PipelineRunVariable("variable", ""))

        # Act
        activities = test_framework.evaluate_activity(for_each_activity, state)

        # Assert
        set_variable_activity = next(activities)
        assert set_variable_activity is not None
        assert set_variable_activity.name == "setVariable"
        # assert set_variable_activity.Value == "a"

        set_variable_activity = next(activities)
        assert set_variable_activity is not None
        assert set_variable_activity.name == "setVariable"
        # assert set_variable_activity.Value == "b"

        set_variable_activity = next(activities)
        assert set_variable_activity is not None
        assert set_variable_activity.name == "setVariable"
        # assert set_variable_activity.Value == "c"

        # Assert that there are no more activities
        try:
            next(activities)
            assert False  # This line should not be reached, an exception should be raised
        except StopIteration:
            pass
