import dataclasses
from typing import Any, Optional


@dataclasses.dataclass(frozen = True)
class EpubMetadataRefine:
    property: str
    value: Any
    scheme: Optional[str] = None
