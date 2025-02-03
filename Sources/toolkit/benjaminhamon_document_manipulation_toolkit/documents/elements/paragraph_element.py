from typing import Iterator

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement


class ParagraphElement(DocumentElement):


    def enumerate_text(self) -> Iterator[TextElement]:
        for child in self.children:
            if isinstance(child, TextElement):
                yield child
