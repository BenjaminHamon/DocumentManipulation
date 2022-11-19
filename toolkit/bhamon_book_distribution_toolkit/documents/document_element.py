from typing import List, Optional


class DocumentElement:


	def __init__(self) -> None:
		self.identifier: Optional[str] = None
		self.style_collection: List[str] = []
		self.children: List["DocumentElement"] = []
