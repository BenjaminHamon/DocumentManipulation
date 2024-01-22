from typing import List, Tuple

from benjaminhamon_book_distribution_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_book_distribution_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_book_distribution_toolkit.epub.epub_package_document import EpubPackageDocument


class EpubPackageConfiguration:


    def __init__(self, package_document: EpubPackageDocument) -> None:
        self.package_document = package_document
        self.content_file_mappings: List[Tuple[str,str]] = []
        self.resource_link_mappings: List[Tuple[str,str]] = []
        self.navigation_items: List[EpubNavigationItem] = []
        self.landmarks: List[EpubLandmark] = []
