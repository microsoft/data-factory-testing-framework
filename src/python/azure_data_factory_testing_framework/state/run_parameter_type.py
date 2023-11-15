from enum import Enum

from azure.core import CaseInsensitiveEnumMeta


class RunParameterType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    Pipeline = "Pipeline"
    Global = "Global"
    Dataset = "Dataset"
    LinkedService = "LinkedService"
