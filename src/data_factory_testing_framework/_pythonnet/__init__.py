import os
from pathlib import Path

import pythonnet

pythonnet.load("coreclr")
import clr  # noqa: E402


def load_dotnet_assemblies() -> None:
    # Load the .NET assemblies
    for dll in (Path(__file__).parent / "bin").glob("**/*.dll"):
        # Pass the path without the ".dll" suffix so pythonnet probes and loads "<path>.dll" directly.
        # With the suffix, pythonnet 3.0.x on .NET 9+ parses the path as an assembly name and fails to load it.
        assembly_path = os.path.splitext(os.path.abspath(dll))[0]
        try:
            clr.AddReference(assembly_path)
        except Exception:
            pass


load_dotnet_assemblies()
