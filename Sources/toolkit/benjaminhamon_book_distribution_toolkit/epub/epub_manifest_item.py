import dataclasses
from typing import List


@dataclasses.dataclass(frozen = True)
class EpubManifestItem:
    identifier: str
    reference: str
    media_type: str
    properties: List[str] = dataclasses.field(default_factory = list)
