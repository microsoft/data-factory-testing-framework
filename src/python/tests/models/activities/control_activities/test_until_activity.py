import pytest

from data_factory_testing_framework.generated.models import ForEachActivity, Expression, ExpressionType, \
    SetVariableActivity, DataFactoryElement, UntilActivity, VariableSpecification
from data_factory_testing_framework.models.base.pipeline_run_variable import PipelineRunVariable
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState
from data_factory_testing_framework.models.test_framework import TestFramework


def test_when_evaluate_until_activity_should_repeat_until_expression_is_true():
    # Arrange
    test_framework = TestFramework()
    until_activity = UntilActivity(name="UntilActivity",
                                   expression=Expression(type=ExpressionType.EXPRESSION, value="@equals(1, 1)"),
                                   activities=[
                                       SetVariableActivity(name="setVariable", variable_name="variable",
                                                           value=DataFactoryElement[str]("'1'"),
                                                           depends_on=[])
                                   ],
                                   depends_on=[])

    state = PipelineRunState(
        variable_specifications={
            "variable": VariableSpecification(type="String")
        }
    )

    # Act
    until_activity.expression.evaluate = lambda state: False
    activities = test_framework.evaluate_activity(until_activity, state)

    # Assert
    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"

    set_variable_activity = next(activities)
    assert set_variable_activity is not None
    assert set_variable_activity.name == "setVariable"

    until_activity.expression.evaluate = lambda state: True

    # Assert that there are no more activities
    with pytest.raises(StopIteration):
        next(activities)
