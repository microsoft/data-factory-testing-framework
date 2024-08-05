from typing import Union

from lark import Token, Transformer, Tree, v_args


@v_args(tree=True)
class DataFactoryExpressionTransformer(Transformer):
    def expression_datafactory_parameters_reference(self, tree: Tree) -> Union[Token, Tree]:
        pipeline_property = tree.children[0]
        variable_name = Token("EXPRESSION_PIPELINE_PROPERTY", f"{pipeline_property}")
        tree = Tree(Token("RULE", "expression_pipeline_reference"), [variable_name])
        return tree
