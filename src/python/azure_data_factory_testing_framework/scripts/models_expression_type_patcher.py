import ast

from azure_data_factory_testing_framework.scripts.utils.ast_utils import transform_ast

if __name__ == "__main__":
    with open("../generated/models/_models_py3_raw.py", "r") as f:
        source_code = f.read()

    # Parse the source code into an abstract syntax tree
    ast_tree = ast.parse(source_code)

    # Apply the transformation to the AST
    transform_ast(ast_tree)

    # Generate modified code from the modified AST
    modified_code = ast.unparse(ast_tree)

    # Write the modified code back to a file
    with open("../generated/models/_models_py3_modified2.py", "w") as f:
        f.write(modified_code)
