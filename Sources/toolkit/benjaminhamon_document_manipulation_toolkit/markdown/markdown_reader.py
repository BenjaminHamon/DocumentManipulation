from typing import List

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.html.html_reader import HtmlReader
from benjaminhamon_document_manipulation_toolkit.interfaces.document_reader import DocumentReader
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_to_html_converter import MarkdownToHtmlConverter


class MarkdownReader(DocumentReader):


    def __init__(self, converter: MarkdownToHtmlConverter, html_reader: HtmlReader) -> None:
        self._converter = converter
        self._html_reader = html_reader


    def read_metadata_from_file(self, document_file_path: str) -> dict:
        raise NotImplementedError


    def read_metadata_from_string(self, document_data: str) -> dict:
        raise NotImplementedError


    def read_content_from_file(self, document_file_path: str) -> RootElement:
        with open(document_file_path, mode = "r", encoding = "utf-8") as document_file:
            document_data = document_file.read()
        return self.read_content_from_string(document_data)


    def read_content_from_string(self, document_data: str) -> RootElement:
        document_as_html_string = self._converter.convert_content(document_data)
        return self._html_reader.read_content_from_string(document_as_html_string)


    def read_comments_from_file(self, document_file_path: str) -> List[DocumentComment]:
        raise NotImplementedError


    def read_comments_from_string(self, document_data: str) -> List[DocumentComment]:
        raise NotImplementedError
