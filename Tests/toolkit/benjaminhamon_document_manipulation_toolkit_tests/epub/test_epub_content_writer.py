""" Unit tests for EpubContentWriter """

# cspell:words dcterms idref itemref lxml oebps opendocument relators rootfile rootfiles

import datetime
import os

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_document_manipulation_toolkit.epub.epub_manifest_item import EpubManifestItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_refine import EpubMetadataRefine
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_document import EpubPackageDocument
from benjaminhamon_document_manipulation_toolkit.epub.epub_spine_item import EpubSpineItem


def test_create_container_as_xml():
    content_writer = EpubContentWriter()
    container_xml = content_writer.create_container_as_xml(os.path.join("EPUB", "content.opf"))

    document_as_string_expected = """
<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

    document_as_string_expected = document_as_string_expected.lstrip()
    document_as_string = lxml.etree.tostring(container_xml,
        doctype = "<?xml version=\"1.0\" encoding=\"utf-8\"?>", encoding = "utf-8", pretty_print = True).decode("utf-8")

    assert document_as_string == document_as_string_expected


def test_convert_package_document_to_xhtml():
    content_writer = EpubContentWriter()

    package_document = EpubPackageDocument()

    package_document.add_minimal_metadata("my-document-identifier", "My Document Title", "en-US")
    package_document.add_modified(datetime.datetime(2020, 1, 1))
    package_document.add_metadata_item(EpubMetadataItem("dc:creator", "My Document Author", xhtml_identifier = "author",
        refines = [ EpubMetadataRefine("role", "aut", "marc:relators") ]))

    package_document.add_manifest_item(
        EpubManifestItem("toc_xhtml", "toc.xhtml", media_type = "application/xhtml+xml", properties = [ "nav" ]))
    package_document.add_manifest_item(
        EpubManifestItem("my_first_section_xhtml", "my_first_section.xhtml", media_type = "application/xhtml+xml"))
    package_document.add_manifest_item(
        EpubManifestItem("my_second_section_xhtml", "my_second_section.xhtml", media_type = "application/xhtml+xml"))

    package_document.add_spine_item(EpubSpineItem("toc_xhtml"))
    package_document.add_spine_item(EpubSpineItem("my_first_section_xhtml"))
    package_document.add_spine_item(EpubSpineItem("my_second_section_xhtml"))

    package_document_as_xml = content_writer.convert_package_document_to_xhtml(package_document, ".")

    document_as_string_expected = """
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="document-identifier">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="document-identifier">my-document-identifier</dc:identifier>
    <dc:title>My Document Title</dc:title>
    <dc:language>en-US</dc:language>
    <meta property="dcterms:modified">2020-01-01T00:00:00Z</meta>
    <dc:creator id="author">My Document Author</dc:creator>
    <meta refines="#author" property="role" scheme="marc:relators">aut</meta>
  </metadata>
  <manifest>
    <item id="toc_xhtml" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="my_first_section_xhtml" href="my_first_section.xhtml" media-type="application/xhtml+xml"/>
    <item id="my_second_section_xhtml" href="my_second_section.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="toc_xhtml" linear="yes"/>
    <itemref idref="my_first_section_xhtml" linear="yes"/>
    <itemref idref="my_second_section_xhtml" linear="yes"/>
  </spine>
</package>
"""

    document_as_string_expected = document_as_string_expected.lstrip()
    document_as_string = lxml.etree.tostring(package_document_as_xml,
        doctype = "<?xml version=\"1.0\" encoding=\"utf-8\"?>", encoding = "utf-8", pretty_print = True).decode("utf-8")

    assert document_as_string == document_as_string_expected
