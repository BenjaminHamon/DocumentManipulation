from typing import Iterator

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement


class RootElement(DocumentElement):


    def get_section_count(self) -> int:
        return sum(1 for _ in self.enumerate_sections())


    def enumerate_sections(self) -> Iterator[SectionElement]:
        for child in self.children:
            if isinstance(child, SectionElement):
                yield child
