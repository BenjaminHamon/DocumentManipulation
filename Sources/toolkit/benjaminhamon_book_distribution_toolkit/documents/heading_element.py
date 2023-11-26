from typing import Iterator, List


from benjaminhamon_book_distribution_toolkit.documents.document_element import DocumentElement
from benjaminhamon_book_distribution_toolkit.documents.document_element_exception import DocumentElementException
from benjaminhamon_book_distribution_toolkit.documents.text_element import TextElement


class HeadingElement(DocumentElement):


    def get_title(self) -> str:
        title_elements: List[str] = []

        for child in self.children:
            if isinstance(child, TextElement) and child.text is not None:
                title_elements.append(child.text)

        if len(title_elements) == 0:
            raise DocumentElementException("HeadingElement has no text")

        return " - ".join(title_elements)


    def enumerate_text(self) -> Iterator[TextElement]:
        for child in self.children:
            if isinstance(child, TextElement):
                yield child
