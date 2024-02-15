import pytest
from data_factory_testing_framework import TestFramework, TestFrameworkType
from data_factory_testing_framework.models import DataFactoryElement, Pipeline
from data_factory_testing_framework.models.activities import SetVariableActivity, SwitchActivity
from data_factory_testing_framework.state import PipelineRunState


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
        id_="some-id",
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
