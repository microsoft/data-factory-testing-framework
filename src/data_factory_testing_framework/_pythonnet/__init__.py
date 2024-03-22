import glob
import os
from pathlib import Path

import pythonnet

import data_factory_testing_framework

pythonnet.load("coreclr")
import clr  # noqa: E402


def load_dotnet_assemblies() -> None:
    # get root of the pyproject path
    package_root = Path(os.path.dirname(data_factory_testing_framework.__file__))
    evaluator_module_path = os.path.join(package_root)
    dlls = glob.glob(f"{evaluator_module_path}/**/*.dll", recursive=True)
    for dll in dlls:
        dll = os.path.abspath(dll)
        try:
            clr.AddReference(dll)
        except Exception:
            pass


load_dotnet_assemblies()
