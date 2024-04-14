# cspell:words dcterms

import datetime
from typing import List, Optional

from benjaminhamon_document_manipulation_toolkit.epub.epub_manifest_item import EpubManifestItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_spine_item import EpubSpineItem


class EpubPackageDocument:


    def __init__(self) -> None:
        self._metadata: List[EpubMetadataItem] = []
        self._manifest: List[EpubManifestItem] = []
        self._spine: List[EpubSpineItem] = []


    def get_identifier(self) -> Optional[EpubMetadataItem]:
        return next((x for x in self._metadata if x.key == "dc:identifier"), None)


    def get_metadata_items(self) -> List[EpubMetadataItem]:
        return list(self._metadata)


    def get_manifest_items(self) -> List[EpubManifestItem]:
        return list(self._manifest)


    def get_spine_items(self) -> List[EpubSpineItem]:
        return list(self._spine)


    def add_minimal_metadata(self, identifier: str, title: str, language: str, modified: datetime.datetime) -> None:
        self.add_metadata_item(EpubMetadataItem("dc:identifier", identifier, xhtml_identifier = "document-identifier"))
        self.add_metadata_item(EpubMetadataItem("dc:title", title))
        self.add_metadata_item(EpubMetadataItem("dc:language", language))
        self.add_metadata_item(EpubMetadataItem("dcterms:modified", modified, is_meta = True))


    def add_metadata_item(self, item_to_add: EpubMetadataItem) -> None:
        self._metadata.append(item_to_add)


    def add_manifest_item(self, item_to_add: EpubManifestItem) -> None:
        existing_item = next((item for item in self._manifest if item.identifier == item_to_add.identifier), None)
        if existing_item is not None:
            raise ValueError("Identifier '%s' already exists in the manifest" % item_to_add.identifier)

        self._manifest.append(item_to_add)


    def set_manifest_item_as_navigation(self, item_identifier: str) -> None:
        referenced_item = next((item for item in self._manifest if item.identifier == item_identifier), None)
        if referenced_item is None:
            raise ValueError("Identifier '%s' does not exist in the manifest" % item_identifier)

        referenced_item.properties.append("nav")


    def set_manifest_item_as_cover_image(self, item_identifier: str) -> None:
        referenced_item = next((item for item in self._manifest if item.identifier == item_identifier), None)
        if referenced_item is None:
            raise ValueError("Identifier '%s' does not exist in the manifest" % item_identifier)

        referenced_item.properties.append("cover-image")


    def add_spine_item(self, item_to_add: EpubSpineItem) -> None:
        referenced_item = next((item for item in self._manifest if item.identifier == item_to_add.reference), None)
        if referenced_item is None:
            raise ValueError("Identifier '%s' does not exist in the manifest" % item_to_add.reference)

        self._spine.append(item_to_add)
