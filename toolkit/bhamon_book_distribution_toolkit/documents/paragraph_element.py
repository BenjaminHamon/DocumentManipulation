from typing import List

from bhamon_book_distribution_toolkit.documents.document_element import DocumentElement
from bhamon_book_distribution_toolkit.documents.text_element import TextElement


class ParagraphElement(DocumentElement):

	
	def enumerate_text(self) -> List[TextElement]:
		for child in self.children:
			if isinstance(child, TextElement):
				yield child
