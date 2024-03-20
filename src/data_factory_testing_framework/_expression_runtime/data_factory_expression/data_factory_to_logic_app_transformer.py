

from typing import Union
from lark import Token, Transformer, Tree, v_args


@v_args(tree=True)
class DataFactoryToLogicaAppTransformer(Transformer):

    def expression_datafactory_activity_reference(self, tree: Tree) -> Union[Token, Tree]:

        #tree = Tree("expression_variable_reference", [tree.children[0], tree.children[1], tree.children[2]])
        # use variable rule with parameter_guid as we know it will be an object
        # variable('parameter_guid').parameters.parameter_name
        # concat children to form a variable name 
        activity_name_token = tree.children[0]
        if not isinstance(activity_name_token, Token):
            raise Exception("Activity name is not a token")
        activity_name = activity_name_token.value[1:-1] # remove the single quotes
        variable_name = Token("EXPRESSION_VARIABLE_NAME", f"'activity_{activity_name}'")
        tree = Tree(
            Token("RULE", "expression_variable_reference"),
            [variable_name])
        return tree

    def expression_datafactory_reference(self, tree: Tree) -> Union[Token, Tree]:
        scope = tree.children[0]
        if not isinstance(scope, Token):
            raise Exception("Scope is not a token")
        scope_value = scope.value

        if scope_value == "pipeline":
            return tree

        variable_name = Token("EXPRESSION_VARIABLE_NAME", f"'{scope_value}'")
        tree = Tree(
            Token("RULE", "expression_variable_reference"),
            [variable_name])
        return tree
    
    def expression_variable_reference(self, tree: Tree) -> Union[Token, Tree]:
        # inject a new 'layer' of the tree
        token = tree.data
        variable_name = tree.children[0] # what if variable name is a tree (i.e. needs to be evaluated)
        variable_name = variable_name[1:-1] # remove the single quotes
        new_variable_name = f"'v_{variable_name}'"
        tree = Tree(
            Token("RULE", "expression_variable_reference"),
            [Token("EXPRESSION_VARIABLE_NAME", new_variable_name)]
        )
        return tree
