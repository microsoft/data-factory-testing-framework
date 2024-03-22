# setup.py
import os
import shutil
from pathlib import Path
from typing import List

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel

dotnet_path = shutil.which("dotnet")


class CustomBuildExtension(Extension):
    def __init__(self, name: str) -> None:
        """Initialize the Extension object."""
        self.source = ""
        super().__init__(name, sources=[], language="csharp")


class BDistWheel(bdist_wheel):
    def get_tag(self) -> List[str]:
        # consider setting bdist parameters instead.
        return (self.python_tag, "none", "any")


class CustomBuildExt(build_ext):
    def run(self) -> None:
        # TODO: need to align with the build_ext command
        self.inplace = False
        super().run()
        for ext in self.extensions:
            self.build(ext)

    def get_ext_filename(self, ext_name: str) -> str:
        return ext_name

    def build(self, ext: Extension) -> None:
        extension_path = Path(self.get_ext_fullpath(ext.name))
        build_dir = Path(self.build_temp)
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        dotnet = dotnet_path

        self.spawn([dotnet, "build", "-c", "Release", "-o", str(extension_path), str(Path(ext.source).parent)])


setup(
    ext_modules=[
        CustomBuildExtension("data_factory_testing_framework.DataFactoryFrameworkEvaluator"),
    ],
    cmdclass={"bdist_wheel": BDistWheel, "build_ext": CustomBuildExt},
)
