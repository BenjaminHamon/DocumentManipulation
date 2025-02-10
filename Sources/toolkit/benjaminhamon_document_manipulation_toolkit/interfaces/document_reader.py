import abc
from typing import List

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement


class DocumentReader(abc.ABC):


    @abc.abstractmethod
    def read_metadata_from_file(self, document_file_path: str) -> dict:
        pass


    @abc.abstractmethod
    def read_metadata_from_string(self, document_data: str) -> dict:
        pass


    @abc.abstractmethod
    def read_content_from_file(self, document_file_path: str) -> RootElement:
        pass


    @abc.abstractmethod
    def read_content_from_string(self, document_data: str) -> RootElement:
        pass


    @abc.abstractmethod
    def read_comments_from_file(self, document_file_path: str) -> List[DocumentComment]:
        pass


    @abc.abstractmethod
    def read_comments_from_string(self, document_data: str) -> List[DocumentComment]:
        pass
