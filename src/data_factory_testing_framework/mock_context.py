
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from data_factory_testing_framework.models._pipeline import Pipeline
    from data_factory_testing_framework.models.activities._activity import Activity




@dataclass
class MockContext:
    pipeline: Optional["Pipeline"] = None
    activity: Optional["Activity"] = None
    property_path: Optional[str] = None
