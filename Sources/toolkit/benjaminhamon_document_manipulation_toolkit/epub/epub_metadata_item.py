import dataclasses
from typing import Any, List, Optional

from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_refine import EpubMetadataRefine


@dataclasses.dataclass(frozen = True)
class EpubMetadataItem:
    key: str
    value: Any
    is_meta: bool = False
    xhtml_identifier: Optional[str] = None
    language: Optional[str] = None
    directionality: Optional[str] = None
    refines: Optional[List[EpubMetadataRefine]] = None
