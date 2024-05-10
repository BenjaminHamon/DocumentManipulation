# cspell:words dcterms

import datetime
import os
import re
from typing import Callable, List, Optional, Tuple, Union

from benjaminhamon_document_manipulation_toolkit import convert_helpers
from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_generation_configuration import EpubGenerationConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.epub.epub_manifest_item import EpubManifestItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation import EpubNavigation
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_configuration import EpubPackageConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_document import EpubPackageDocument
from benjaminhamon_document_manipulation_toolkit.epub.epub_spine_item import EpubSpineItem


def create_package_configuration(
        epub_generation_configuration: EpubGenerationConfiguration, source_directory_for_epub_files: str) -> EpubPackageConfiguration:

    builder = EpubPackageConfigurationBuilder()
    builder.add_metadata(epub_generation_configuration.metadata, "{modified}")
    builder.add_main_files(source_directory_for_epub_files)
    if epub_generation_configuration.cover_file is not None:
        builder.add_cover(epub_generation_configuration.cover_file)
    builder.add_content_files(epub_generation_configuration.content_files)
    builder.add_resource_files(epub_generation_configuration.resource_files)
    builder.add_link_overrides(epub_generation_configuration.link_overrides)
    builder.add_landmarks(epub_generation_configuration.landmarks)

    return builder.get_configuration()


class EpubPackageConfigurationBuilder:


    def __init__(self) -> None:
        self._package_document = EpubPackageDocument()
        self._content_configuration = EpubContentConfiguration()
        self._navigation = EpubNavigation()


    def get_configuration(self) -> EpubPackageConfiguration:
        return EpubPackageConfiguration(self._package_document, self._content_configuration, self._navigation)


    def add_metadata(self, metadata: List[EpubMetadataItem], modified: Union[str,datetime.datetime]) -> None:
        for metadata_item in metadata:
            self._package_document.add_metadata_item(metadata_item)
        self._package_document.add_modified(modified)


    def add_main_files(self, source_directory: str) -> None:
        self._content_configuration.file_mappings.append((os.path.join(source_directory, "content.opf"), os.path.join("EPUB", "content.opf")))
        self._content_configuration.file_mappings.append((os.path.join(source_directory, "toc.xhtml"), os.path.join("EPUB", "toc.xhtml")))
        self._content_configuration.file_mappings.append((os.path.join(source_directory, "container.xml"), os.path.join("META-INF", "container.xml")))
        self._package_document.add_manifest_item(EpubManifestItem("toc", "EPUB/toc.xhtml", "application/xhtml+xml", [ "nav" ]))


    def add_cover(self, source_file_path: str) -> None:
        file_extension = os.path.splitext(source_file_path)[1]

        manifest_item = EpubManifestItem(
            identifier = "cover",
            reference = "EPUB/cover" + file_extension,
            media_type = epub_xhtml_helpers.get_media_type(source_file_path))

        self._package_document.add_manifest_item(manifest_item)
        self._package_document.set_manifest_item_as_cover_image(manifest_item.identifier)
        self._content_configuration.file_mappings.append((source_file_path, os.path.join("EPUB", "cover" + file_extension)))


    def add_content_files(self, content_file_collection: List[str], title_getter: Optional[Callable[[str],str]] = None) -> None:

        def get_title_from_xhtml(xhtml_file_path) -> str:
            xhtml_document = epub_xhtml_helpers.load_xhtml(xhtml_file_path)
            return epub_xhtml_helpers.get_xhtml_title(xhtml_document)

        if title_getter is None:
            title_getter = get_title_from_xhtml

        file_count = len(content_file_collection)

        for file_index, source_file_path in enumerate(content_file_collection):
            file_name = re.sub(r"^[0-9]+ - ", "", os.path.basename(source_file_path))
            file_name = document_operations.generate_section_file_name(file_name, file_index, file_count)
            destination_file_path = os.path.join("EPUB", "Content", convert_helpers.sanitize_for_file_name_and_href(file_name))
            reference = destination_file_path.replace("\\", "/")
            identifier = convert_helpers.sanitize_for_identifier(file_name)
            media_type = epub_xhtml_helpers.get_media_type(reference)
            title = title_getter(source_file_path)

            self._package_document.add_manifest_item(EpubManifestItem(identifier, reference, media_type))
            self._package_document.add_spine_item(EpubSpineItem(identifier))
            self._content_configuration.file_mappings.append((source_file_path, destination_file_path))
            self._navigation.navigation_items.append(EpubNavigationItem(reference, title))


    def add_resource_files(self, resource_file_collection: List[str]) -> None:
        for source_file_path in resource_file_collection:
            file_name = os.path.basename(source_file_path)
            destination_file_path = os.path.join("EPUB", "Resources", convert_helpers.sanitize_for_file_name_and_href(file_name))
            link_before = source_file_path.replace("\\", "/")
            link_after = destination_file_path.replace("\\", "/")
            identifier = convert_helpers.sanitize_for_identifier(file_name)
            media_type = epub_xhtml_helpers.get_media_type(link_after)

            self._package_document.add_manifest_item(EpubManifestItem(identifier, link_after, media_type))
            self._content_configuration.file_mappings.append((source_file_path, destination_file_path))
            self._content_configuration.link_mappings.append((link_before, link_after))


    def add_link_overrides(self, link_override_collection: List[Tuple[str,str]]) -> None:
        for link_override in reversed(link_override_collection):
            self._content_configuration.link_mappings.insert(0, link_override)


    def add_landmarks(self, landmark_collection: List[EpubLandmark]) -> None:
        for landmark in landmark_collection:
            landmark_resolved = EpubLandmark(
                epub_type = landmark.epub_type,
                reference = self._resolve_navigation_reference(landmark.reference),
                display_name = landmark.display_name)

            self._navigation.landmarks.append(landmark_resolved)


    def _resolve_navigation_reference(self, reference: str) -> str:
        file_name_to_search = convert_helpers.sanitize_for_file_name_and_href(os.path.basename(reference))

        for navigation_item in self._navigation.navigation_items:
            file_name = re.sub(r"^[0-9]+_-_", "", os.path.basename(navigation_item.reference))
            if file_name == file_name_to_search:
                return navigation_item.reference

        raise ValueError("Reference not found: '%s'" % reference)
