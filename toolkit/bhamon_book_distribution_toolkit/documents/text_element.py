import dataclasses
from typing import Optional

from bhamon_book_distribution_toolkit.documents.document_element import DocumentElement


class TextElement(DocumentElement):


	def __init__(self) -> None:
		super().__init__()

		self.text: Optional[str] = None
