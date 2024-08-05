from pathlib import Path as _Path

from data_factory_testing_framework._test_framework import TestFramework, TestFrameworkType

try:
    root = _Path(__file__).parent
    with open(root / "VERSION") as version_file:
        version = version_file.read().strip()
except FileNotFoundError:
    # Set a default version (for local builds)
    version = "0.0.0.dev0"

__all__ = ["TestFramework", "TestFrameworkType"]
__version__ = version
