from typing import List

from bhamon_book_distribution_toolkit.epub.epub_manifest_item import EpubManifestItem


class EpubManifest:


	def __init__(self) -> None:
		self._item_collection: List[EpubManifestItem] = []
		self._spine: List[str] = []


	def get_item_collection(self) -> List[EpubManifestItem]:
		return list(self._item_collection)


	def get_spine(self) -> List[str]:
		return list(self._spine)


	def add_item(self, item_to_add: EpubManifestItem) -> None:
		existing_item = next((x for x in self._item_collection if x.identifier == item_to_add.identifier), None)
		if existing_item is not None:
			raise ValueError("Identifier '%s' is around present in the manifest" % item_to_add.identifier)

		self._item_collection.append(item_to_add)


	def add_spine_element(self, item_identifier: str) -> None:
		self._spine.append(item_identifier)


	def get_media_type(self, file_path: str) -> str:
		if file_path.endswith(".css"):
			return "text/css"
		if file_path.endswith(".xhtml"):
			return "application/xhtml+xml"
		if file_path.endswith(".ncx"):
			return "application/x-dtbncx+xml"

		raise ValueError("Unsupported file type: '%s'" % file_path)
