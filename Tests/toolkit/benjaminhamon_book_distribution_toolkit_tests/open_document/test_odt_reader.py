# cspell:words fodt lxml

""" Unit tests for OdtReader """

import datetime
import os

import lxml.etree

from benjaminhamon_book_distribution_toolkit.open_document.odt_reader import OdtReader


def test_read_metadata_from_fodt():
    fodt_file_path = os.path.join(os.path.dirname(__file__), "empty.fodt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    fodt_data = odt_reader.read_fodt(fodt_file_path)
    document_metadata = odt_reader.read_metadata(fodt_data)

    assert document_metadata["title"] == "My Document"
    assert document_metadata["author"] == "Benjamin Hamon"
    assert document_metadata["revision"] == 1
    assert document_metadata["creation_date"] is not None
    assert document_metadata["creation_date"].tzinfo == datetime.timezone.utc
    assert document_metadata["update_date"] is not None
    assert document_metadata["update_date"].tzinfo == datetime.timezone.utc


def test_read_metadata_from_odt():
    odt_file_path = os.path.join(os.path.dirname(__file__), "empty.odt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    odt_data = odt_reader.read_odt(odt_file_path, "meta.xml")
    document_metadata = odt_reader.read_metadata(odt_data)

    assert document_metadata["title"] == "My Document"
    assert document_metadata["author"] == "Benjamin Hamon"
    assert document_metadata["revision"] == 1
    assert document_metadata["creation_date"] is not None
    assert document_metadata["creation_date"].tzinfo == datetime.timezone.utc
    assert document_metadata["update_date"] is not None
    assert document_metadata["update_date"].tzinfo == datetime.timezone.utc
