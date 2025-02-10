from typing import List

import lxml.html.html5parser

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.html.html_to_document_converter import HtmlToDocumentConverter
from benjaminhamon_document_manipulation_toolkit.interfaces.document_reader import DocumentReader


class HtmlReader(DocumentReader):


    def __init__(self, converter: HtmlToDocumentConverter, parser: lxml.html.html5parser.HTMLParser) -> None:
        self._converter = converter
        self._parser = parser


    def read_metadata_from_file(self, document_file_path: str) -> dict:
        raise NotImplementedError


    def read_metadata_from_string(self, document_data: str) -> dict:
        raise NotImplementedError


    def read_content_from_file(self, document_file_path: str) -> RootElement:
        with open(document_file_path, mode = "r", encoding = "utf-8") as document_file:
            document_data = document_file.read()
        return self.read_content_from_string(document_data)


    def read_content_from_string(self, document_data: str) -> RootElement:
        document_as_xml = self._parser.parse(document_data)
        return self._converter.convert_content(document_as_xml)


    def read_comments_from_file(self, document_file_path: str) -> List[DocumentComment]:
        raise NotImplementedError


    def read_comments_from_string(self, document_data: str) -> List[DocumentComment]:
        raise NotImplementedError
