from benjaminhamon_document_manipulation_toolkit.documents.document_element import DocumentElement


class TextElement(DocumentElement):


    def __init__(self, text: str) -> None:
        super().__init__()

        self.text: str = text
        self.line_break: bool = False
