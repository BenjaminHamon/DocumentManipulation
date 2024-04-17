from benjaminhamon_document_manipulation_toolkit.documents.document_element import DocumentElement


class TextRegionStartElement(DocumentElement):


    def __init__(self, identifier: str) -> None:
        super().__init__()
        self.identifier = identifier
