from unittest.mock import Mock

import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.exceptions._control_activity_expression_evaluated_not_to_expected_type import (
    ControlActivityExpressionEvaluatedNotToExpectedTypeError,
)
from data_factory_testing_framework.models import DataFactoryElement, DataFactoryObjectType, Pipeline
from data_factory_testing_framework.models.activities import SetVariableActivity, SwitchActivity
from data_factory_testing_framework.state import PipelineRunState, PipelineRunVariable, RunParameter, RunParameterType


def test_when_evaluated_should_evaluate_expression() -> None:
    # Arrange
    activity = SwitchActivity(
        name="SwitchActivity",
        default_activities=[],
        cases_activities={},
        typeProperties={"on": DataFactoryElement("@concat('case_', '1')")},
    )

    # Act
    activity.evaluate(PipelineRunState())

    # Assert
    assert activity.on.result == "case_1"


@pytest.mark.parametrize(
    "on_value,expected_outcome",
    [
        ("case_1", "case_1_hit"),
        ("case_2", "case_2_hit"),
        ("case_3", "default_hit"),
        ("case_4", "default_hit"),
        ("case_anything", "default_hit"),
    ],
)
def test_correct_case_evaluated(on_value: str, expected_outcome: str) -> None:
    # Arrange
    test_framework = TestFramework(framework_type=TestFrameworkType.Fabric)
    pipeline = Pipeline(
        pipeline_id="some-id",
        name="pipeline",
        variables={
            "variable": {
                "type": "String",
                "defaultValue": "",
            },
        },
        activities=[
            SwitchActivity(
                name="SwitchActivity",
                default_activities=[
                    SetVariableActivity(
                        name="setVariableActivity1",
                        typeProperties={
                            "variableName": "variable",
                            "value": "default_hit",
                        },
                    ),
                ],
                cases_activities={
                    "case_1": [
                        SetVariableActivity(
                            name="setVariableActivity2",
                            typeProperties={
                                "variableName": "variable",
                                "value": "case_1_hit",
                            },
                        ),
                    ],
                    "case_2": [
                        SetVariableActivity(
                            name="setVariableActivity3",
                            typeProperties={
                                "variableName": "variable",
                                "value": "case_2_hit",
                            },
                        ),
                    ],
                },
                typeProperties={"on": DataFactoryElement(on_value)},
            )
        ],
    )

    # Act
    activity = next(test_framework.evaluate_pipeline(pipeline, []))

    # Assert
    assert activity.type == "SetVariable"
    assert activity.type_properties["value"] == expected_outcome


def test_evaluate_pipeline_should_pass_iteration_item_to_child_activities() -> None:
    # Arrange
    state = PipelineRunState(variables=[PipelineRunVariable("variable", None)], iteration_item="some-item")
    activity = SwitchActivity(
        name="SwitchActivity",
        default_activities=[],
        cases_activities={},
        typeProperties={"on": DataFactoryElement("on-expr")},
    )
    evaluator = Mock(return_value=[])

    # Act
    list(activity.evaluate_control_activities(state, evaluator))

    # Assert
    assert evaluator.call_args[0][1].iteration_item == "some-item"


@pytest.mark.parametrize(("evaluated_value"), [1, 1.1, True, {}, [], None])
def test_evaluated_raises_error_when_evaluated_value_is_not_a_str(evaluated_value: DataFactoryObjectType) -> None:
    # Arrange
    state = PipelineRunState(parameters=[RunParameter(RunParameterType.Pipeline, "input_values", evaluated_value)])
    activity = SwitchActivity(
        name="SwitchActivity",
        default_activities=[],
        cases_activities={},
        typeProperties={"on": DataFactoryElement("@pipeline().parameters.input_values")},
    )

    # Act
    with pytest.raises(ControlActivityExpressionEvaluatedNotToExpectedTypeError) as ex_info:
        activity.evaluate(state)

    assert (
        ex_info.value.args[0]
        == "Iteration expression of Activity: 'SwitchActivity' does not evaluate to the expected type: 'str'."
    )
