import dataclasses
from typing import Any, List, Optional

from benjaminhamon_book_distribution_toolkit.epub.epub_metadata_refine import EpubMetadataRefine


@dataclasses.dataclass(frozen = True)
class EpubMetadataItem:
    key: str
    value: Any
    is_meta: bool = False
    xhtml_identifier: Optional[str] = None
    refine_collection: List[EpubMetadataRefine] = dataclasses.field(default_factory = list)
