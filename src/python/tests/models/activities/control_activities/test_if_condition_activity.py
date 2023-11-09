import pytest

from data_factory_testing_framework.generated.models import ForEachActivity, Expression, ExpressionType, \
    SetVariableActivity, DataFactoryElement, IfConditionActivity
from data_factory_testing_framework.models.base.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.models.test_framework import TestFramework


class TestIfConditionActivity:

    def test_when_evaluated_should_evaluate_expression(self):
        # Arrange
        activity = IfConditionActivity(
            name="IfConditionActivity",
            expression=Expression(type=ExpressionType.EXPRESSION, value="@equals(1, 1)"))

        # Act
        activity.evaluate(PipelineRunState())

        # Assert
        # assert activity.expression.evaluated == True

    @pytest.mark.parametrize("expression_outcome,expected_activity_name", [(True, "setVariableActivity1"),(False, "setVariableActivity2")])
    def test_when_evaluated_should_evaluate_correct_child_activities(self, expression_outcome, expected_activity_name):
        # Arrange
        test_framework = TestFramework()
        expression = "@equals(1, 1)" if expression_outcome else "@equals(1, 2)"
        activity = IfConditionActivity(
            name="IfConditionActivity",
            expression=Expression(type=ExpressionType.EXPRESSION, value=expression),
            if_true_activities=[
                SetVariableActivity(
                    name="setVariableActivity1",
                    variable_name="variable",
                    value="dummy")
            ],
            if_false_activities=[
                SetVariableActivity(
                    name="setVariableActivity2",
                    variable_name="variable",
                    value="dummy")
            ]
        )

        state = PipelineRunState()
        state.variables.append(PipelineRunVariable("variable", ""))

        # Act
        child_activities = list(test_framework.evaluate_activity(activity, state))

        # Assert
        assert len(child_activities) == 1
        assert child_activities[0].name == expected_activity_name
