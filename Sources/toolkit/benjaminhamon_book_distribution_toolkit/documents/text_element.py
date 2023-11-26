from benjaminhamon_book_distribution_toolkit.documents.document_element import DocumentElement


class TextElement(DocumentElement):


    def __init__(self, text: str) -> None:
        super().__init__()

        self.text: str = text
