import glob
import os

import pythonnet

pythonnet.load("coreclr")
import clr  # noqa: E402


def load_dotnet_assemblies() -> None:
    path = os.path.join(os.path.dirname(__file__), "DataFactoryTestingFrameworkEvaluator", "net8.0")
    dlls = glob.glob(f"{path}/**/*.dll", recursive=True)
    for dll in dlls:
        dll = os.path.abspath(dll)
        try:
            clr.AddReference(dll)
        except Exception:
            pass


load_dotnet_assemblies()
