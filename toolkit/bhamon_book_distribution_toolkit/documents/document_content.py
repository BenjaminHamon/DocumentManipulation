import dataclasses
from typing import List

from bhamon_book_distribution_toolkit.documents.section_element import SectionElement


@dataclasses.dataclass
class DocumentContent:
	sections: List[SectionElement] = dataclasses.field(default_factory = list)
