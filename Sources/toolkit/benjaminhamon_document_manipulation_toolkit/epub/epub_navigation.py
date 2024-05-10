import dataclasses
from typing import List

from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_item import EpubNavigationItem


@dataclasses.dataclass()
class EpubNavigation:
    navigation_items: List[EpubNavigationItem] = dataclasses.field(default_factory = list)
    landmarks: List[EpubLandmark] = dataclasses.field(default_factory = list)
