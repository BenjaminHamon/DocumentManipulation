import dataclasses
import datetime
from typing import List, Optional

from bhamon_book_distribution_toolkit.documents.document_content import DocumentContent


@dataclasses.dataclass
class Document:
	identifier: str
	title: str
	authors: List[str]
	language: Optional[str] = None
	identifier_for_epub: Optional[str] = None
	revision: Optional[str] = None
	revision_date: Optional[datetime.datetime] = None
	content: Optional[DocumentContent] = None
