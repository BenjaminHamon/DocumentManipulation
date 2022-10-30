import dataclasses
from typing import Optional


@dataclasses.dataclass
class TextElement:
	text: str
	style: Optional[str] = None
