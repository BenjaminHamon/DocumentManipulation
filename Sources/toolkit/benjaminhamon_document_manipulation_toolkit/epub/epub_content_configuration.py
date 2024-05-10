import dataclasses
from typing import List, Tuple


@dataclasses.dataclass()
class EpubContentConfiguration:
    file_mappings: List[Tuple[str,str]] = dataclasses.field(default_factory = list)
    link_mappings: List[Tuple[str,str]] = dataclasses.field(default_factory = list)
