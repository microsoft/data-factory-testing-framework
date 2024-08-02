"""Custom build script for building the C# project with setuptools.

Based on the following discussion: https://github.com/pypa/setuptools/discussions/3762
"""
import shutil
import subprocess
from contextlib import suppress
from pathlib import Path

from setuptools import Command, setup
from setuptools.command.build import build


class CustomCommand(Command):
    def initialize_options(self) -> None:
        self.pkg_name = self.distribution.get_name().replace("-", "_")
        self.bdist_dir = None

    def finalize_options(self) -> None:
        with suppress(Exception):
            self.bdist_dir = Path(self.get_finalized_command("bdist_wheel").bdist_dir)

    def run(self) -> None:
        if self.bdist_dir:
            dotnet_path = shutil.which("dotnet")
        output_dir = self.bdist_dir / self.pkg_name / "_pythonnet" / "bin"
        output_dir.mkdir(parents=True, exist_ok=True)

        if dotnet_path is None:
            raise Exception("dotnet not found")

        subprocess.check_call(
            [
                dotnet_path,
                "build",
                "-c",
                "Release",
                "-o",
                str(output_dir),
                Path("src", self.pkg_name, "_pythonnet", "Evaluator.csproj"),
            ]
        )


class CustomBuild(build):
    sub_commands = [("build_custom", None)] + build.sub_commands


try:
    root = Path(__file__).parent
    with open(root / "VERSION") as version_file:
        version = version_file.read().strip()
except FileNotFoundError:
    # Set a default version (for local builds)
    version = "0.0.0.dev0"

setup(cmdclass={"build": CustomBuild, "build_custom": CustomCommand}, version=version)
