from typing import List, Tuple

from benjaminhamon_book_distribution_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_book_distribution_toolkit.epub.epub_navigation_item import EpubNavigationItem


class EpubPackageConfiguration:


    def __init__(self) -> None:
        self.content_file_mappings: List[Tuple[str,str]] = []
        self.resource_link_mappings: List[Tuple[str,str]] = []
        self.navigation_items: List[EpubNavigationItem] = []
        self.landmarks: List[EpubLandmark] = []
