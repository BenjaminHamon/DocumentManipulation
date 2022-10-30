import dataclasses
from typing import List, Optional

from bhamon_book_distribution_toolkit.documents.document_content import DocumentContent


@dataclasses.dataclass
class Document:
	identifier: str
	title: str
	authors: List[str]
	language: Optional[str] = None
	identifier_for_epub: Optional[str] = None
	content: Optional[DocumentContent] = None
