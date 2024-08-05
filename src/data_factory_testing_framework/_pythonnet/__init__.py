import os
from pathlib import Path

import pythonnet

pythonnet.load("coreclr")
import clr  # noqa: E402


def load_dotnet_assemblies() -> None:
    # Load the .NET assemblies
    for dll in (Path(__file__).parent / "bin").glob("**/*.dll"):
        dll = os.path.abspath(dll)
        try:
            clr.AddReference(dll)
        except Exception:
            pass


load_dotnet_assemblies()
