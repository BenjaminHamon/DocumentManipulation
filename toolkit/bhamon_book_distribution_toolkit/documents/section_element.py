import dataclasses
from typing import List, Optional

from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement


@dataclasses.dataclass
class SectionElement:
	title: str
	sections: List["SectionElement"] = dataclasses.field(default_factory = list)
	paragraphs: List[ParagraphElement] = dataclasses.field(default_factory = list)
	style: Optional[str] = None
