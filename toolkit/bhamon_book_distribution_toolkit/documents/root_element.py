from typing import List

from bhamon_book_distribution_toolkit.documents.document_element import DocumentElement
from bhamon_book_distribution_toolkit.documents.section_element import SectionElement


class RootElement(DocumentElement):


	def enumerate_sections(self) -> List[SectionElement]:
		for child in self.children:
			if isinstance(child, SectionElement):
				yield child
