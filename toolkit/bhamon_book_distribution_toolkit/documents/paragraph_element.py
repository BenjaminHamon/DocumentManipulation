import dataclasses
from typing import List, Optional

from bhamon_book_distribution_toolkit.documents.text_element import TextElement


@dataclasses.dataclass
class ParagraphElement:
	text_elements: List[TextElement] = dataclasses.field(default_factory = list)
	style: Optional[str] = None
