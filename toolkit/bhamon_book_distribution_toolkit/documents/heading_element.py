from typing import Optional

from bhamon_book_distribution_toolkit.documents.document_element import DocumentElement
from bhamon_book_distribution_toolkit.documents.document_element_exception import DocumentElementException
from bhamon_book_distribution_toolkit.documents.text_element import TextElement


class HeadingElement(DocumentElement):
	

	def __init__(self) -> None:
		super().__init__()

		self.level_in_tree: Optional[int] = None
		self.category: Optional[str] = None
		self.index_in_category: Optional[int] = None


	def get_text(self) -> TextElement:
		if isinstance(self.children[0], TextElement):
			return self.children[0]

		raise DocumentElementException("HeadingElement has no text")
