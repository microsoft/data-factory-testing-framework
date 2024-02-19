import pythonnet

pythonnet.load("coreclr")
import glob
import os

import clr


def load_dotnet_assemblies():
    path = os.path.join(os.path.dirname(__file__), "DataFactoryTestingFrameworkEvaluator", "net8.0")
    print(f"Loading .NET assemblies from {path}")

    dlls = glob.glob(f"{path}/**/*.dll", recursive=True)
    print(f"Loading {len(dlls)} .NET assemblies")
    for dll in dlls:
        dll = os.path.abspath(dll)
        try:
            clr.AddReference(dll)
        except Exception as e:
            print(f"Error adding reference to {dll}: {e}")
            pass


load_dotnet_assemblies()
