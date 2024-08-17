from enum import Enum

from data_factory_testing_framework._enum_meta import CaseInsensitiveEnumMeta


class DependencyCondition(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """DependencyCondition."""

    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    COMPLETED = "Completed"
