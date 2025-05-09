from enum import Enum

from data_factory_testing_framework._enum_meta import CaseInsensitiveEnumMeta


class RunParameterType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    Pipeline = "Pipeline"
    Global = "Global"
    Dataset = "Dataset"
    LinkedService = "LinkedService"
    System = "System"
    LibraryVariables = "LibraryVariables"

    def __str__(self) -> str:
        """Get the string representation of the enum.

        We override this method to make sure that the string representation
        is the same across all Python versions.

        Returns:
            The string representation of the enum.
        """
        super().__str__()
        return f"{RunParameterType.__name__}.{self.name}"
