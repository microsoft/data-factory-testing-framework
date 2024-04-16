from enum import Enum
from typing import Iterator, List, Optional

from azure.core import CaseInsensitiveEnumMeta

from data_factory_testing_framework._repositories._factories.data_factory_repository_factory import (
    DataFactoryRepositoryFactory,
)
from data_factory_testing_framework._repositories._factories.fabric_repository_factory import (
    FabricRepositoryFactory,
)
from data_factory_testing_framework._repositories.data_factory_repository import DataFactoryRepository
from data_factory_testing_framework.exceptions import (
    NoRemainingPipelineActivitiesMeetDependencyConditionsError,
)
from data_factory_testing_framework.models import Pipeline
from data_factory_testing_framework.models.activities import (
    Activity,
    ControlActivity,
    ExecutePipelineActivity,
    FailActivity,
    ForEachActivity,
    IfConditionActivity,
    SwitchActivity,
    UntilActivity,
)
from data_factory_testing_framework.state import PipelineRunState, RunParameter


class TestFrameworkType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """TestFrameworkType."""

    __test__ = False  # Prevent pytest from discovering this class as a test class

    DataFactory = "DataFactory"
    Fabric = "Fabric"
    Synapse = "Synapse"


class TestFramework:
    __test__ = False  # Prevent pytest from discovering this class as a test class

    def __init__(
        self,
        framework_type: TestFrameworkType,
        root_folder_path: Optional[str] = None,
        should_evaluate_child_pipelines: Optional[bool] = False,
    ) -> None:
        """Initializes the test framework allowing you to evaluate pipelines and activities.

        Args:
            framework_type: type of the test framework.
            root_folder_path: optional path to the folder containing the data factory files.
            The repository attribute will be populated with the data factory entities if provided.
            should_evaluate_child_pipelines: optional boolean indicating whether child pipelines should be evaluated. Defaults to False.
        """
        self._framework_type = framework_type

        if self._framework_type == TestFrameworkType.Fabric:
            if root_folder_path is not None:
                self._repository = FabricRepositoryFactory().parse_from_folder(root_folder_path)
            else:
                self._repository = DataFactoryRepository([])
        elif self._framework_type == TestFrameworkType.DataFactory:
            if root_folder_path is not None:
                self._repository = DataFactoryRepositoryFactory().parse_from_folder(root_folder_path)
            else:
                self._repository = DataFactoryRepository([])
        elif self._framework_type == TestFrameworkType.Synapse:
            raise NotImplementedError("Synapse test framework is not implemented yet.")

        self._should_evaluate_child_pipelines = should_evaluate_child_pipelines

    @property
    def framework_type(self) -> TestFrameworkType:
        """Indicates which test framework is used.

        Returns:
            A TestFrameworkType object.
        """
        return self._framework_type

    @property
    def should_evaluate_child_pipelines(self) -> bool:
        """Indicates whether child pipelines should be evaluated.

        Returns:
            A boolean indicating whether child pipelines should be evaluated.
        """
        return self._should_evaluate_child_pipelines

    def evaluate_activity(self, activity: Activity, state: PipelineRunState) -> Iterator[Activity]:
        """Evaluates a single activity given a state. Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activity: The activity to evaluate.
            state: The state to use for evaluating the activity.

        Returns:
             A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        return self.evaluate_activities([activity], state)

    def evaluate_pipeline(self, pipeline: Pipeline, parameters: List[RunParameter]) -> Iterator[Activity]:
        """Evaluates all pipeline activities using the provided parameters.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            pipeline: The pipeline to evaluate.
            parameters: The parameters to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        parameters = pipeline.validate_and_append_default_parameters(parameters)
        state = PipelineRunState(parameters, pipeline.get_run_variables())
        return self.evaluate_activities(pipeline.activities, state)

    def evaluate_activities(self, activities: List[Activity], state: PipelineRunState) -> Iterator[Activity]:
        """Evaluates all activities using the provided state.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activities: The activities to evaluate.
            state: The state to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        fail_activity_evaluated = False
        while len(state.scoped_activity_results) != len(activities):
            any_activity_evaluated = False
            for activity in filter(
                lambda a: state.is_activity_evaluated_in_scope(a.name) is False
                and a.are_dependency_condition_met(state),
                activities,
            ):
                evaluated_activity = activity.evaluate(state)
                if not self._is_iteration_activity(evaluated_activity) or (
                    isinstance(evaluated_activity, ExecutePipelineActivity) and not self.should_evaluate_child_pipelines
                ):
                    yield evaluated_activity

                if isinstance(activity, FailActivity):
                    fail_activity_evaluated = True
                    break

                any_activity_evaluated = True
                state.add_activity_result(activity.name, activity.status, activity.output)

                # Check if there are any child activities to evaluate
                if self._is_iteration_activity(activity):
                    activities_iterator = []
                    if isinstance(activity, ExecutePipelineActivity) and self.should_evaluate_child_pipelines:
                        execute_pipeline_activity: ExecutePipelineActivity = activity
                        pipeline: Pipeline = None
                        if self.framework_type == TestFrameworkType.Fabric:
                            pipeline = self.get_pipeline_by_id(
                                # Note: in the future they will probably rename this to referenceId for Fabric
                                execute_pipeline_activity.type_properties["pipeline"]["referenceName"],
                            )
                        else:
                            pipeline = self.get_pipeline_by_name(
                                execute_pipeline_activity.type_properties["pipeline"]["referenceName"],
                            )
                        activities_iterator = execute_pipeline_activity.evaluate_pipeline(
                            pipeline,
                            activity.get_child_run_parameters(state),
                            self.evaluate_activities,
                        )

                    if not isinstance(activity, ExecutePipelineActivity) and isinstance(activity, ControlActivity):
                        control_activity: ControlActivity = activity
                        activities_iterator = control_activity.evaluate_control_activities(
                            state,
                            self.evaluate_activities,
                        )

                    for child_activity in activities_iterator:
                        yield child_activity
                        if isinstance(child_activity, FailActivity):
                            fail_activity_evaluated = True
                            break

            if fail_activity_evaluated:
                break

            if not any_activity_evaluated:
                raise NoRemainingPipelineActivitiesMeetDependencyConditionsError()

    def get_pipeline_by_name(self, name: str) -> Pipeline:
        """Gets a pipeline by name.

        Args:
            name: The name of the pipeline to get.

        Returns:
            The pipeline with the given name.
        """
        return self._repository.get_pipeline_by_name(name)

    def get_pipeline_by_id(self, pipeline_id: str) -> Pipeline:
        """Get a pipeline by id. Throws an exception if the pipeline is not found.

        Args:
            pipeline_id: The identifier of the pipeline to get.

        Returns:
            The pipeline with the given id.
        """
        return self._repository.get_pipeline_by_id(pipeline_id)

    @staticmethod
    def _is_iteration_activity(activity: Activity) -> bool:
        return (
            isinstance(activity, UntilActivity)
            or isinstance(activity, ForEachActivity)
            or isinstance(activity, IfConditionActivity)
            or isinstance(activity, SwitchActivity)
            or isinstance(activity, ExecutePipelineActivity)
        )
