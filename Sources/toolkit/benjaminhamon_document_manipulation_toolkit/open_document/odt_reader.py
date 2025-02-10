# cspell:words fodt lxml

import zipfile
from typing import List

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.interfaces.document_reader import DocumentReader
from benjaminhamon_document_manipulation_toolkit.open_document.odt_to_document_converter import OdtToDocumentConverter


class OdtReader(DocumentReader):


    def __init__(self, converter: OdtToDocumentConverter, xml_parser: lxml.etree.XMLParser) -> None:
        self._converter = converter
        self._xml_parser = xml_parser


    def read_metadata_from_file(self, document_file_path: str) -> dict:
        document_data = self._read_odt(document_file_path, "meta.xml")
        return self.read_metadata_from_string(document_data)


    def read_metadata_from_string(self, document_data: str) -> dict:
        odt_as_xml = lxml.etree.fromstring(document_data, self._xml_parser)
        return self._converter.convert_metadata(odt_as_xml)


    def read_content_from_file(self, document_file_path: str) -> RootElement:
        document_data = self._read_odt(document_file_path, "content.xml")
        return self.read_content_from_string(document_data)


    def read_content_from_string(self, document_data: str) -> RootElement:
        odt_as_xml = lxml.etree.fromstring(document_data, self._xml_parser)
        return self._converter.convert_content(odt_as_xml)


    def read_comments_from_file(self, document_file_path: str) -> List[DocumentComment]:
        document_data = self._read_odt(document_file_path, "content.xml")
        return self.read_comments_from_string(document_data)


    def read_comments_from_string(self, document_data: str) -> List[DocumentComment]:
        odt_as_xml = lxml.etree.fromstring(document_data, self._xml_parser)
        return self._converter.convert_comments(odt_as_xml)


    def _read_odt(self, odt_file_path: str, file_path_in_archive: str) -> str:

        def strip_encoding_declaration(xml_data: str) -> str:
            if not xml_data.startswith("<?xml "):
                return xml_data

            xml_data_start_index = xml_data.index("<", 1)
            return xml_data[xml_data_start_index:]

        if odt_file_path.endswith(".fodt"):
            with open(odt_file_path, mode = "r", encoding = "utf-8") as fodt_file:
                return strip_encoding_declaration(fodt_file.read())

        if odt_file_path.endswith(".odt"):
            with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
                return strip_encoding_declaration(odt_file.read(file_path_in_archive).decode("utf-8"))

        raise ValueError("File extension should be fodt or odt: '%s'" % odt_file_path)
