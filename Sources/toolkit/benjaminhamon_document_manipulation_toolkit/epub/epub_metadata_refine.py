import dataclasses
from typing import Any, Optional


@dataclasses.dataclass(frozen = True)
class EpubMetadataRefine:
    key: str
    value: Any
    scheme: Optional[str] = None
