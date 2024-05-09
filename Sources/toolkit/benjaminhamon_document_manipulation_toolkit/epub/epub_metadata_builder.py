# cspell:words relators

import datetime
from typing import List, Optional

from benjaminhamon_document_manipulation_toolkit import urn_helpers
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.metadata import marc_relator_conversion
from benjaminhamon_document_manipulation_toolkit.metadata.dc_contributor import DcContributor
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_refine import EpubMetadataRefine


def create_epub_metadata_from_document_information(document_information: DocumentInformation) -> List[EpubMetadataItem]:
    builder = EpubMetadataBuilder()

    if document_information.identifier is not None:
        builder.add_identifier(document_information.identifier, "metadata-identifier")

    if document_information.title is not None:
        builder.add_title(document_information.title)

    if document_information.language is not None:
        builder.add_language(document_information.language)

    if document_information.author is not None:
        builder.add_creator(DcContributor(document_information.author))

    if document_information.publication_date is not None:
        builder.add_date(document_information.publication_date)

    if document_information.publisher is not None:
        builder.add_publisher(document_information.publisher)

    return builder.build()


def create_epub_metadata_from_dc_metadata(dc_metadata: DcMetadata) -> List[EpubMetadataItem]: # pylint: disable = too-many-branches
    builder = EpubMetadataBuilder()

    if dc_metadata.identifiers is not None:
        if len(dc_metadata.identifiers) > 0:
            builder.add_identifier(dc_metadata.identifiers[0], "metadata-identifier")
        for extra_identifier in dc_metadata.identifiers[1:]:
            builder.add_identifier(extra_identifier)

    if dc_metadata.titles is not None:
        for title in dc_metadata.titles:
            builder.add_title(title)

    if dc_metadata.languages is not None:
        for language in dc_metadata.languages:
            builder.add_language(language)

    if dc_metadata.contributors is not None:
        for contributor in dc_metadata.contributors:
            builder.add_contributor(contributor)

    if dc_metadata.creators is not None:
        for creator in dc_metadata.creators:
            builder.add_creator(creator)

    if dc_metadata.dates is not None:
        for date in dc_metadata.dates:
            builder.add_date(date)

    if dc_metadata.publishers is not None:
        for publisher in dc_metadata.publishers:
            builder.add_publisher(publisher)

    if dc_metadata.subjects is not None:
        for subject in dc_metadata.subjects:
            builder.add_subject(subject)

    if dc_metadata.document_types is not None:
        for document_type in dc_metadata.document_types:
            builder.add_type(document_type)

    return builder.build()


class EpubMetadataBuilder:


    def __init__(self) -> None:
        self._metadata_items: List[EpubMetadataItem] = []


    def build(self) -> List[EpubMetadataItem]:
        return self._metadata_items


    def add_identifier(self, identifier: str, xhtml_identifier: Optional[str] = None) -> None:
        identifier_as_urn = urn_helpers.convert_identifier_to_urn(identifier)
        self._metadata_items.append(EpubMetadataItem(key = "dc:identifier", value = identifier_as_urn, xhtml_identifier = xhtml_identifier))


    def add_title(self, title: str) -> None:
        self._metadata_items.append(EpubMetadataItem(key = "dc:title", value = title))


    def add_language(self, language: str) -> None:
        self._metadata_items.append(EpubMetadataItem(key = "dc:language", value = language))


    def add_contributor(self, contributor: DcContributor, key: Optional[str] = None, xhtml_identifier: Optional[str] = None) -> None:
        if key is None:
            key = "dc:contributor"

        refines: List[EpubMetadataRefine] = []
        if contributor.role is not None:
            if xhtml_identifier is None:
                xhtml_identifier = "metadata-" + contributor.role.lower().replace(" ", "-")
            role_code = marc_relator_conversion.convert_term_to_code(contributor.role)
            refines.append(EpubMetadataRefine(property = "role", value = role_code, scheme = "marc:relators"))

        if contributor.file_as is not None:
            refines.append(EpubMetadataRefine(property = "file-as", value = contributor.file_as))

        if xhtml_identifier is None and len(refines) > 0:
            raise ValueError("xhtml_identifier is required with refines")

        self._metadata_items.append(
            EpubMetadataItem(key = key, value = contributor.name, xhtml_identifier = xhtml_identifier, refines = refines if len(refines) > 0 else None))


    def add_creator(self, creator: DcContributor, xhtml_identifier: Optional[str] = None) -> None:
        self.add_contributor(creator, "dc:creator", xhtml_identifier)


    def add_date(self, date: datetime.date) -> None:
        self._metadata_items.append(EpubMetadataItem(key = "dc:date", value = date))


    def add_publisher(self, publisher: str) -> None:
        self._metadata_items.append(EpubMetadataItem(key = "dc:publisher", value = publisher))


    def add_subject(self, subject: str) -> None:
        self._metadata_items.append(EpubMetadataItem(key = "dc:subject", value = subject))


    def add_type(self, document_type: str) -> None:
        self._metadata_items.append(EpubMetadataItem(key = "dc:type", value = document_type))
