from typing import Any, List

from data_factory_testing_framework.generated.models import Activity, DependencyCondition, PipelineResource, \
    UntilActivity, ForEachActivity, IfConditionActivity, ExecutePipelineActivity, ControlActivity

from data_factory_testing_framework.models.repositories.data_factory_repository_factory import \
    DataFactoryRepositoryFactory
from data_factory_testing_framework.models.state.pipeline_run_state import PipelineRunState


class TestFramework:

    def __init__(self, data_factory_folder_path: str = None, should_evaluate_child_pipelines: bool = False):
        self.repository = data_factory_folder_path is not None and DataFactoryRepositoryFactory.parse_from_folder(data_factory_folder_path)
        self.should_evaluate_child_pipelines = should_evaluate_child_pipelines

    def evaluate_activity(self, activity: Activity, state: PipelineRunState) -> List[Activity]:
        return self.evaluate_activities([activity], state)

    def evaluate_pipeline(self, pipeline: PipelineResource, state: PipelineRunState) -> List[Activity]:
        return self.evaluate_activities(pipeline.activities, state)

    def evaluate_activities(self, activities: List[Activity], state: PipelineRunState) -> List[Activity]:
        while len(state.scoped_pipeline_activity_results) != len(activities):
            any_activity_evaluated = False
            for activity in filter(
                    lambda a: a not in state.scoped_pipeline_activity_results and a.are_dependency_condition_met(state),
                    activities):
                evaluated_activity = activity.evaluate(state)
                if not self._is_iteration_activity(evaluated_activity) or (isinstance(evaluated_activity, ExecutePipelineActivity) and not self.should_evaluate_child_pipelines):
                    yield evaluated_activity

                any_activity_evaluated = True
                state.add_activity_result(activity)

                if self._is_iteration_activity(activity):
                    if isinstance(activity, ExecutePipelineActivity) and self.should_evaluate_child_pipelines:
                        execute_pipeline_activity: ExecutePipelineActivity = activity
                        pipeline = self.repository.get_pipeline_by_name(execute_pipeline_activity.pipeline.reference_name)

                        # Evaluate the pipeline with its own scope
                        for childActivity in self.evaluate_pipeline(pipeline, activity.get_child_run_parameters(state)):
                            yield childActivity

                    if isinstance(activity, ControlActivity):
                        control_activity: ControlActivity = activity
                        for childActivity in control_activity.evaluate_control_activity_iterations(state, self.evaluate_activities):
                            yield childActivity

            if not any_activity_evaluated:
                raise Exception(
                    "Validate that there are no circular dependencies or whether activity results were not set correctly.")

    @staticmethod
    def _is_iteration_activity(activity: Activity) -> bool:
        return (isinstance(activity, UntilActivity) or
                isinstance(activity, ForEachActivity) or
                isinstance(activity, IfConditionActivity) or
                isinstance(activity, ExecutePipelineActivity))
