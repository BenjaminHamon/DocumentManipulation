import dataclasses
from typing import List, Optional

from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem


@dataclasses.dataclass()
class EpubMetadata:
    xhtml_identifier_for_unique_identifier: Optional[str] = None
    items: List[EpubMetadataItem] = dataclasses.field(default_factory = list)
