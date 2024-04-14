import dataclasses
from typing import List


@dataclasses.dataclass(frozen = True)
class EpubSpineItem:
    reference: str
    is_linear: bool = True
    properties: List[str] = dataclasses.field(default_factory = list)
