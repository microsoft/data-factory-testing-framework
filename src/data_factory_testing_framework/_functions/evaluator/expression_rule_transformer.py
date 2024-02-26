from lark import Transformer, Tree, v_args

from data_factory_testing_framework._functions.evaluator.rules import (
    ActivityReferenceExpressionRuleEvaluator,
    BranchExpressionRuleEvaluator,
    DatasetReferenceExpressionRuleEvaluator,
    EvaluationExpressionRuleEvaluator,
    ExpressionParameterExpressionRuleEvaluator,
    ExpressionRuleEvaluator,
    FunctionCallExpressionRuleEvaluator,
    ItemReferenceExpressionRuleEvaluator,
    LinkedServiceReferenceExpressionRuleEvaluator,
    LiteralEvaluationExpressionRuleEvaluator,
    LiteralInterpolationExpressionRuleEvaluator,
    LogicalBoolExpressionEvaluator,
    PipelineReferenceExpressionRuleEvaluator,
    SystemVariableReferenceExpressionRuleEvaluator,
    VariableReferenceExpressionRuleEvaluator,
)
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState


@v_args(tree=True)
class ExpressionRuleTransformer(Transformer[ExpressionRuleEvaluator]):
    def __init__(self, state: PipelineRunState) -> None:  # noqa: D107
        visit_tokens = False
        self.state: PipelineRunState = state
        super().__init__(visit_tokens)

    def expression_pipeline_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return PipelineReferenceExpressionRuleEvaluator(tree, self.state)

    def expression_logical_bool(self, tree: Tree) -> ExpressionRuleEvaluator:
        return LogicalBoolExpressionEvaluator(tree)

    def expression_branch(self, tree: Tree) -> ExpressionRuleEvaluator:
        return BranchExpressionRuleEvaluator(tree)

    def expression_evaluation(self, tree: Tree) -> ExpressionRuleEvaluator:
        return EvaluationExpressionRuleEvaluator(tree)

    def expression_function_call(self, tree: Tree) -> ExpressionRuleEvaluator:
        return FunctionCallExpressionRuleEvaluator(tree)

    def expression_item_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return ItemReferenceExpressionRuleEvaluator(tree, self.state)

    def expression_system_variable_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return SystemVariableReferenceExpressionRuleEvaluator(tree, self.state)

    def expression_activity_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return ActivityReferenceExpressionRuleEvaluator(tree, self.state)

    def expression_linked_service_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return LinkedServiceReferenceExpressionRuleEvaluator(tree, self.state)

    def expression_dataset_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return DatasetReferenceExpressionRuleEvaluator(tree, self.state)

    def expression_variable_reference(self, tree: Tree) -> ExpressionRuleEvaluator:
        return VariableReferenceExpressionRuleEvaluator(tree, self.state)

    def literal_interpolation(self, tree: Tree) -> ExpressionRuleEvaluator:
        return LiteralInterpolationExpressionRuleEvaluator(tree)

    def literal_evaluation(self, tree: Tree) -> ExpressionRuleEvaluator:
        return LiteralEvaluationExpressionRuleEvaluator(tree)

    def expression_parameter(self, tree: Tree) -> ExpressionRuleEvaluator:
        return ExpressionParameterExpressionRuleEvaluator(tree)

    def __default__(self, data, children, meta):  # noqa: ANN204, D105, ANN001
        raise ValueError(f"Unknown expression rule with data: {data}, children: {children}, meta: {meta}")
