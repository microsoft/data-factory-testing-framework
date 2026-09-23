from pathlib import Path

import pythonnet

pythonnet.load("coreclr")
import clr  # noqa: E402


def load_dotnet_assemblies() -> None:
    # Load the .NET assemblies
    for dll in (Path(__file__).parent / "bin").glob("**/*.dll"):
        # clr.AddReference appends the file extension itself when resolving a path,
        # so the path has to be passed without the '.dll' suffix.
        assembly_path = str(dll.resolve().with_suffix(""))
        try:
            clr.AddReference(assembly_path)
        except Exception:
            pass


load_dotnet_assemblies()
