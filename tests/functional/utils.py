import inspect


def is_public_module(module: object) -> bool:
    if not inspect.ismodule(module):
        return False
    # only get the last part of the module name
    module_name = module.__name__.split(".")[-1]
    return not module_name.startswith("_")
