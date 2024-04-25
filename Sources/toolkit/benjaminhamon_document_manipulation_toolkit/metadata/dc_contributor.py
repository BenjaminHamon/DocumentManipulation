# cspell:words fodt

import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen = True)
class DcContributor:
    name: str
    role: Optional[str] = None
    file_as: Optional[str] = None
