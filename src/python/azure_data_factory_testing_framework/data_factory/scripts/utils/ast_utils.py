import ast
from _ast import Load, Name

from azure_data_factory_testing_framework.scripts.utils.docstring_utils import (
    parse_restructured_docstring,
)

target_type = "DataFactoryElement"


def get_type_from_description(description: str) -> str:
    dfe_type = "str"
    if "Expression with resultType string" in description:
        dfe_type = "str"
    if "Expression with resultType integer" in description:
        dfe_type = "int"
    if "Expression with resultType boolean" in description:
        dfe_type = "bool"

    return dfe_type


def update_attribute_type(arg: ast.arg, description: str) -> None:
    dfe_type = get_type_from_description(description)
    if "Expression" in description:
        if (
            hasattr(arg.annotation, "value")
            and arg.annotation.value.id == "Optional"
            and hasattr(arg.annotation.slice, "id")
            and arg.annotation.slice.id == "JSON"
        ):
            arg.annotation.slice = ast.Subscript(
                value=Name("DataFactoryElement", ctx=Load()),
                slice=Name(dfe_type, ctx=Load()),
                ctx=Load(),
            )

        if hasattr(arg.annotation, "id") and arg.annotation.id == "JSON":
            arg.annotation = ast.Subscript(
                value=Name("DataFactoryElement", ctx=Load()),
                slice=Name(dfe_type, ctx=Load()),
                ctx=Load(),
            )


def transform_ast(node: ast.ClassDef) -> None:
    if isinstance(node, ast.ClassDef):
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                for arg in body_item.args.kwonlyargs:
                    if (
                        arg.annotation
                        and isinstance(arg.annotation, ast.Name)
                        or isinstance(arg.annotation.value, ast.Name)
                    ):
                        docstring = parse_restructured_docstring(ast.get_docstring(node))
                        for param_doc in docstring["params"]:
                            if param_doc["name"] == arg.arg:
                                update_attribute_type(arg, param_doc["doc"])

    for child in ast.iter_child_nodes(node):
        transform_ast(child)
