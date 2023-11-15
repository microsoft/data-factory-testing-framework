from typing import List

from azure_data_factory_testing_framework.exceptions.pipeline_activities_circular_dependency_error import (
    PipelineActivitiesCircularDependencyError,
)
from azure_data_factory_testing_framework.generated.models import (
    Activity,
    ControlActivity,
    ExecutePipelineActivity,
    ForEachActivity,
    IfConditionActivity,
    PipelineResource,
    UntilActivity,
)
from azure_data_factory_testing_framework.models import DataFactoryRepositoryFactory
from azure_data_factory_testing_framework.models.repositories.data_factory_repository import DataFactoryRepository
from azure_data_factory_testing_framework.state import PipelineRunState, RunParameter


class TestFramework:
    def __init__(self, data_factory_folder_path: str = None, should_evaluate_child_pipelines: bool = False) -> None:
        """Initializes the test framework allowing you to evaluate pipelines and activities.

        Args:
            data_factory_folder_path: optional path to the folder containing the data factory files.
            The repository attribute will be populated with the data factory entities if provided.
            should_evaluate_child_pipelines: optional boolean indicating whether child pipelines should be evaluated. Defaults to False.
        """
        if data_factory_folder_path is not None:
            self.repository = DataFactoryRepositoryFactory.parse_from_folder(data_factory_folder_path)
        else:
            self.repository = DataFactoryRepository([])

        self.should_evaluate_child_pipelines = should_evaluate_child_pipelines

    def evaluate_activity(self, activity: Activity, state: PipelineRunState) -> List[Activity]:
        """Evaluates a single activity given a state. Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activity: The activity to evaluate.
            state: The state to use for evaluating the activity.

        Returns:
             A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        return self.evaluate_activities([activity], state)

    def evaluate_pipeline(self, pipeline: PipelineResource, parameters: List[RunParameter]) -> List[Activity]:
        """Evaluates all pipeline activities using the provided parameters.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            pipeline: The pipeline to evaluate.
            parameters: The parameters to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        pipeline.validate_parameters(parameters)
        state = PipelineRunState(parameters, pipeline.variables)
        return self.evaluate_activities(pipeline.activities, state)

    def evaluate_activities(self, activities: List[Activity], state: PipelineRunState) -> List[Activity]:
        """Evaluates all activities using the provided state.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activities: The activities to evaluate.
            state: The state to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        while len(state.scoped_pipeline_activity_results) != len(activities):
            any_activity_evaluated = False
            for activity in filter(
                    lambda a: a.name not in state.scoped_pipeline_activity_results
                              and a.are_dependency_condition_met(state),
                    activities,
            ):
                evaluated_activity = activity.evaluate(state)
                if not self._is_iteration_activity(evaluated_activity) or (
                        isinstance(evaluated_activity,
                                   ExecutePipelineActivity) and not self.should_evaluate_child_pipelines
                ):
                    yield evaluated_activity

                any_activity_evaluated = True
                state.add_activity_result(activity.name, activity.status)

                if self._is_iteration_activity(activity):
                    if isinstance(activity, ExecutePipelineActivity) and self.should_evaluate_child_pipelines:
                        execute_pipeline_activity: ExecutePipelineActivity = activity
                        pipeline = self.repository.get_pipeline_by_name(
                            execute_pipeline_activity.pipeline.reference_name,
                        )

                        # Evaluate the pipeline with its own scope
                        for child_activity in self.evaluate_pipeline(
                                pipeline,
                                activity.get_child_run_parameters(state),
                        ):
                            yield child_activity

                    if isinstance(activity, ControlActivity):
                        control_activity: ControlActivity = activity
                        for child_activity in control_activity.evaluate_control_activity_iterations(
                                state,
                                self.evaluate_activities,
                        ):
                            yield child_activity

            if not any_activity_evaluated:
                raise PipelineActivitiesCircularDependencyError()

    @staticmethod
    def _is_iteration_activity(activity: Activity) -> bool:
        return (
                isinstance(activity, UntilActivity)
                or isinstance(activity, ForEachActivity)
                or isinstance(activity, IfConditionActivity)
                or isinstance(activity, ExecutePipelineActivity)
        )
