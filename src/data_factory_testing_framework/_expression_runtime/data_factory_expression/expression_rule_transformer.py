from typing import Union

from data_factory_testing_framework._expression_runtime.data_factory_expression.rules import (
    ActivityReferenceExpressionRuleEvaluator,
    DatasetReferenceExpressionRuleEvaluator,
    ExpressionRuleEvaluator,
    ItemReferenceExpressionRuleEvaluator,
    LinkedServiceReferenceExpressionRuleEvaluator,
    PipelineReferenceExpressionRuleEvaluator,
    SystemVariableReferenceExpressionRuleEvaluator,
    VariableReferenceExpressionRuleEvaluator,
)
from data_factory_testing_framework._expression_runtime.data_factory_expression.rules.literal_interpolation_expression_rule_evaluator import (
    LiteralInterpolationExpressionRuleEvaluator,
)
from data_factory_testing_framework.state._pipeline_run_state import PipelineRunState
from lark import Token, Transformer, Tree, v_args


@v_args(tree=True)
class ExpressionRuleTransformer(Transformer[ExpressionRuleEvaluator]):
    def __init__(self, state: PipelineRunState) -> None:  # noqa: D107
        visit_tokens = False
        self.state: PipelineRunState = state
        super().__init__(visit_tokens)

    def start(self, tree: Tree) -> Tree:
        return self._try_convert_expression_to_literal_tree(tree)

    def expression_start(self, tree: Tree) -> Tree:
        return self._try_convert_expression_to_literal_tree(tree)

    def expression_evaluation(self, tree: Tree) -> Tree:
        if self._is_tree_purely_an_expression_tree(tree):
            return tree.children[0]

        return tree

    def expression_call(self, tree: Tree) -> Tree:
        if self._is_tree_purely_an_expression_tree(tree):
            return tree.children[0]

        return tree

    def expression_pipeline_reference(self, tree: Tree) -> Union[Token, Tree]:
        return PipelineReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def expression_item_reference(self, tree: Tree) -> Union[Token, Tree]:
        return ItemReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def expression_system_variable_reference(self, tree: Tree) -> Union[Token, Tree]:
        return SystemVariableReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def expression_activity_reference(self, tree: Tree) -> Union[Token, Tree]:
        return ActivityReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def expression_linked_service_reference(self, tree: Tree) -> Union[Token, Tree]:
        return LinkedServiceReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def expression_dataset_reference(self, tree: Tree) -> Union[Token, Tree]:
        return DatasetReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def expression_variable_reference(self, tree: Tree) -> Union[Token, Tree]:
        return VariableReferenceExpressionRuleEvaluator(tree, self.state).evaluate_and_transform()

    def literal_interpolation(self, tree: Tree) -> Union[Token, Tree]:
        return LiteralInterpolationExpressionRuleEvaluator(tree).evaluate_and_transform()

    def expression_logical_bool(self, tree: Tree) -> ExpressionRuleEvaluator:
        return tree

    def expression_branch(self, tree: Tree) -> ExpressionRuleEvaluator:
        return tree

    @staticmethod
    def _try_convert_expression_to_literal_tree(tree: Tree) -> Tree:
        """Converts the expression tree to a literal tree if an expression tree is at the root of the tree."""
        if (
            len(tree.children) == 1
            and hasattr(tree.children[0], "type")
            and tree.children[0].type.startswith("EXPRESSION_")
        ):
            child = tree.children[0]

            if child.type == "EXPRESSION_STRING":
                return Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_LETTER", child.value[1:-1])])
            if child.type == "EXPRESSION_INTEGER":
                return Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_INT", child.value)])
            if child.type == "EXPRESSION_FLOAT":
                return Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_FLOAT", child.value)])
            if child.type == "EXPRESSION_BOOLEAN":
                return Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_BOOLEAN", child.value)])
            if child.type == "EXPRESSION_NULL":
                return Tree(Token("RULE", "literal_evaluation"), [Token("LITERAL_NULL", child.value)])

            raise ValueError(f"Unknown expression_evaluation child type: {child.type}")

        return tree

    @staticmethod
    def _is_tree_purely_an_expression_tree(tree: Tree) -> bool:
        return (
            len(tree.children) == 1
            and hasattr(tree.children[0], "type")
            and tree.children[0].type.startswith("EXPRESSION_")
        )
