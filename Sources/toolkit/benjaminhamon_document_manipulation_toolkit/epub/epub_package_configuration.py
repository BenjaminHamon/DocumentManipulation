import dataclasses

from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation import EpubNavigation
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_document import EpubPackageDocument


@dataclasses.dataclass()
class EpubPackageConfiguration:
    document: EpubPackageDocument
    content_configuration: EpubContentConfiguration
    navigation: EpubNavigation
