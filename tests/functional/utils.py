import inspect
from typing import Callable


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


def is_public_class(class_: object) -> bool:
    if not inspect.isclass(class_):
        return False
    return not class_.__name__.startswith("_")


def get_public_members(inspectable: object, predicate: Callable) -> list[str]:
    member_names = [module[0] for module in inspect.getmembers(inspectable, predicate=predicate)]
    # getmembers filters with predicate on the actual class - for modules we need to filter names again
    return list(filter(lambda x: not x.startswith("_"), member_names))


def is_property(method: object) -> bool:
    if isinstance(method, property):
        return True
    return False
