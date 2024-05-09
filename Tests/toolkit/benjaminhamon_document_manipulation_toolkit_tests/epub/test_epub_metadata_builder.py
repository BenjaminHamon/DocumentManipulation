""" Unit tests for epub_metadata_conversion """

# cspell:words relators

from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.epub import epub_metadata_builder
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_refine import EpubMetadataRefine
from benjaminhamon_document_manipulation_toolkit.metadata.dc_contributor import DcContributor
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata


def test_create_epub_metadata_from_document_information():
    document_information = DocumentInformation(
        identifier = "ISBN 000-0-0000000-0-0",
        title = "Some Title",
        language = "en-US",
        author = "Some Author")

    epub_metadata = epub_metadata_builder.create_epub_metadata_from_document_information(document_information)

    epub_metadata_expected = [
        EpubMetadataItem("dc:identifier", "urn:isbn:0000000000000", xhtml_identifier = "metadata-identifier"),
        EpubMetadataItem("dc:title", "Some Title"),
        EpubMetadataItem("dc:language", "en-US"),
        EpubMetadataItem("dc:creator", "Some Author"),
    ]

    assert epub_metadata == epub_metadata_expected


def test_create_epub_metadata_from_dc_metadata():
    dc_metadata = DcMetadata(
        identifiers = [ "ISBN 000-0-0000000-0-0" ],
        titles = [ "Some Title" ],
        languages = [ "en-US" ],
        creators = [ DcContributor("Some Author", "Author", "Author, Some") ])

    epub_metadata = epub_metadata_builder.create_epub_metadata_from_dc_metadata(dc_metadata)

    epub_metadata_expected = [
        EpubMetadataItem("dc:identifier", "urn:isbn:0000000000000", xhtml_identifier = "metadata-identifier"),
        EpubMetadataItem("dc:title", "Some Title"),
        EpubMetadataItem("dc:language", "en-US"),
        EpubMetadataItem("dc:creator", "Some Author",
            refines = [ EpubMetadataRefine("role", "aut", "marc:relators"), EpubMetadataRefine("file-as", "Author, Some") ],
            xhtml_identifier = "metadata-author"),
    ]

    assert epub_metadata == epub_metadata_expected
