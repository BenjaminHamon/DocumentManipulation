# cspell:words dcterms

import dataclasses
import glob
from typing import List, Optional, Tuple

from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem


@dataclasses.dataclass()
class EpubGenerationConfiguration:
    metadata: List[EpubMetadataItem] = dataclasses.field(default_factory = list)
    cover_file: Optional[str] = None
    content_files: List[str] = dataclasses.field(default_factory = list)
    resource_files: List[str] = dataclasses.field(default_factory = list)
    link_overrides: List[Tuple[str,str]] = dataclasses.field(default_factory = list)
    landmarks: List[EpubLandmark] = dataclasses.field(default_factory = list)


    def resolve_file_patterns(self) -> None:
        content_file_collection_resolved: List[str] = []
        for file_path in self.content_files:
            content_file_collection_resolved += glob.glob(file_path)

        resource_file_collection_resolved: List[str] = []
        for file_path in self.resource_files:
            resource_file_collection_resolved += glob.glob(file_path)

        self.content_files = content_file_collection_resolved
        self.resource_files = resource_file_collection_resolved
