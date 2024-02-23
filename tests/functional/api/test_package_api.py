import inspect

from tests.functional.utils import is_public_module


def test_package_root() -> None:
    # Arrange

    # Act
    import data_factory_testing_framework as package

    # Assert
    assert package.__name__ == "data_factory_testing_framework"


def test_package_modules() -> None:
    # Arrange
    import data_factory_testing_framework as package

    # Act
    public_modules = [module[0] for module in inspect.getmembers(package, predicate=is_public_module)]

    # Assert
    assert len(public_modules) == 3
    assert public_modules == ["exceptions", "models", "state"]


def test_package_classes() -> None:
    # Arrange
    import data_factory_testing_framework as package

    # Act
    public_classes = [module[0] for module in inspect.getmembers(package, predicate=inspect.isclass)]

    # Assert
    assert len(public_classes) == 3
    assert public_classes == ["FunctionsRepository", "TestFramework", "TestFrameworkType"]


def test_package_exceptions() -> None:
    # Arrange
    import data_factory_testing_framework.exceptions as module

    # Act
    public_modules = [module[0] for module in inspect.getmembers(module, predicate=is_public_module)]

    # Assert
    assert len(public_modules) == 0


def test_package_exceptions_classes() -> None:
    # Arrange
    import data_factory_testing_framework.exceptions as module

    # Act
    public_classes = [module[0] for module in inspect.getmembers(module, predicate=inspect.isclass)]

    # Assert
    assert len(public_classes) == 11
    assert public_classes == [
        "ActivityNotFoundError",
        "ActivityOutputFieldNotFoundError",
        "DataFactoryElementEvaluationError",
        "FunctionCallInvalidArgumentsCountError",
        "NoRemainingPipelineActivitiesMeetDependencyConditionsError",
        "ParameterNotFoundError",
        "PipelineNotFoundError",
        "StateIterationItemNotSetError",
        "UnsupportedFunctionError",
        "VariableBeingEvaluatedDoesNotExistError",
        "VariableNotFoundError",
    ]


def test_package_models() -> None:
    # Arrange
    import data_factory_testing_framework.models as module

    # Act
    public_modules = [module[0] for module in inspect.getmembers(module, predicate=is_public_module)]

    # Assert
    assert len(public_modules) == 1
    assert public_modules == ["activities"]


def test_package_models_classes() -> None:
    # Arrange
    import data_factory_testing_framework.models as module

    # Act
    public_classes = [module[0] for module in inspect.getmembers(module, predicate=inspect.isclass)]

    # Assert
    assert len(public_classes) == 2
    assert public_classes == ["DataFactoryElement", "Pipeline"]


def test_package_models_activities() -> None:
    # Arrange
    import data_factory_testing_framework.models.activities as module

    # Act
    public_modules = [module[0] for module in inspect.getmembers(module, predicate=is_public_module)]

    # Assert
    assert len(public_modules) == 0


def test_package_models_activities_classes() -> None:
    # Arrange
    import data_factory_testing_framework.models.activities as module

    # Act
    public_classes = [module[0] for module in inspect.getmembers(module, predicate=inspect.isclass)]

    # Assert
    assert len(public_classes) == 12
    assert public_classes == [
        "Activity",
        "ActivityDependency",
        "AppendVariableActivity",
        "ControlActivity",
        "ExecutePipelineActivity",
        "FailActivity",
        "FilterActivity",
        "ForEachActivity",
        "IfConditionActivity",
        "SetVariableActivity",
        "SwitchActivity",
        "UntilActivity",
    ]


def test_package_state() -> None:
    # Arrange
    import data_factory_testing_framework.state as module

    # Act
    public_modules = [module[0] for module in inspect.getmembers(module, predicate=is_public_module)]

    # Assert
    assert len(public_modules) == 0
    assert public_modules == []


def test_package_state_classes() -> None:
    # Arrange
    import data_factory_testing_framework.state as module

    # Act
    public_classes = [module[0] for module in inspect.getmembers(module, predicate=inspect.isclass)]

    # Assert
    assert len(public_classes) == 7
    assert public_classes == [
        "ActivityResult",
        "DependencyCondition",
        "PipelineRunState",
        "PipelineRunVariable",
        "RunParameter",
        "RunParameterType",
        "RunState",
    ]
