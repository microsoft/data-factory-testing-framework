import inspect


def is_public_module(module: object) -> bool:
    if not inspect.ismodule(module):
        return False
    # only get the last part of the module name
    module_name = module.__name__.split(".")[-1]
    return not module_name.startswith("_")


def is_public_method(method: object) -> bool:
    if not inspect.isfunction(method):
        return False
    return method.__name__ == "__init__" or not method.__name__.startswith("_")


def is_property(method: object) -> bool:
    if isinstance(method, property):
        return True
    return False
