from typing import List

from bhamon_book_distribution_toolkit.documents.document_element import DocumentElement
from bhamon_book_distribution_toolkit.documents.document_element_exception import DocumentElementException
from bhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement


class SectionElement(DocumentElement):


	def get_heading(self) -> HeadingElement:
		if isinstance(self.children[0], HeadingElement):
			return self.children[0]

		raise DocumentElementException("SectionElement has no heading")

	
	def enumerate_paragraphs(self) -> List[ParagraphElement]:
		for child in self.children:
			if isinstance(child, ParagraphElement):
				yield child


	def enumerate_subsections(self) -> List["SectionElement"]:
		for child in self.children:
			if isinstance(child, SectionElement):
				yield child
