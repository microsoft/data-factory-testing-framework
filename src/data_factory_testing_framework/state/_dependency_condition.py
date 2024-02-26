from enum import Enum

from azure.core import CaseInsensitiveEnumMeta


class DependencyCondition(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """DependencyCondition."""

    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    COMPLETED = "Completed"
