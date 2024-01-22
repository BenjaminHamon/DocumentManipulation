# cspell:words dcterms

import os
import re
from typing import List, Tuple
import urllib.parse

from benjaminhamon_book_distribution_toolkit import convert_helpers
from benjaminhamon_book_distribution_toolkit.documents import document_operations
from benjaminhamon_book_distribution_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_book_distribution_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_book_distribution_toolkit.epub.epub_manifest_item import EpubManifestItem
from benjaminhamon_book_distribution_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_book_distribution_toolkit.epub.epub_metadata_refine import EpubMetadataRefine
from benjaminhamon_book_distribution_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_book_distribution_toolkit.epub.epub_package_configuration import EpubPackageConfiguration
from benjaminhamon_book_distribution_toolkit.epub.epub_package_document import EpubPackageDocument
from benjaminhamon_book_distribution_toolkit.epub.epub_spine_item import EpubSpineItem


def create_package_configuration(configuration_as_dict: dict) -> EpubPackageConfiguration:
    package_document = EpubPackageDocument()
    epub_configuration = EpubPackageConfiguration(package_document)

    update_document_metadata(package_document, configuration_as_dict["package_metadata"])

    if configuration_as_dict.get("cover_file", None) is not None:
        add_cover(package_document, epub_configuration, configuration_as_dict["cover_file"])

    if configuration_as_dict.get("information_file", None) is not None:
        add_information(package_document, epub_configuration, configuration_as_dict["information_file"], len(configuration_as_dict["content_file_collection"]))

    add_content_files(package_document, epub_configuration, configuration_as_dict["content_file_collection"])
    add_resource_files(package_document, epub_configuration, configuration_as_dict["resource_file_collection"])
    add_navigation(package_document, epub_configuration, configuration_as_dict.get("landmarks", []))

    return epub_configuration


def update_document_metadata(package_document: EpubPackageDocument, metadata_as_dict: dict) -> None:
    for metadata_item_as_dict in metadata_as_dict:
        package_document.add_metadata_item(create_metadata_item(metadata_item_as_dict))

    package_document.add_metadata_item(EpubMetadataItem("dcterms:modified", "{modified}", is_meta = True))


def create_metadata_item(metadata_item_as_dict: dict) -> EpubMetadataItem:
    return EpubMetadataItem(
        key = metadata_item_as_dict["key"],
        value = metadata_item_as_dict["value"],
        is_meta = metadata_item_as_dict.get("is_meta", False),
        xhtml_identifier = metadata_item_as_dict.get("xhtml_identifier", None),
        refine_collection = [ create_metadata_refine(metadata_refine_as_dict) for metadata_refine_as_dict in metadata_item_as_dict.get("refines", []) ])


def create_metadata_refine(metadata_refine_as_dict: dict) -> EpubMetadataRefine:
    return EpubMetadataRefine(
        key = metadata_refine_as_dict["key"],
        value = metadata_refine_as_dict["value"],
        scheme = metadata_refine_as_dict.get("scheme", None),
    )


def add_cover(
        package_document: EpubPackageDocument,
        epub_configuration: EpubPackageConfiguration,
        source_file_path: str) -> None:

    file_extension = os.path.splitext(source_file_path)[1]
    destination_file_path = "cover" + file_extension

    reference = destination_file_path
    identifier = convert_helpers.sanitize_for_identifier(reference)
    media_type = epub_xhtml_helpers.get_media_type(reference)

    package_document.add_manifest_item(EpubManifestItem(identifier, reference, media_type))
    package_document.set_manifest_item_as_cover_image(identifier)

    epub_configuration.content_file_mappings.append((source_file_path, destination_file_path))


def add_information(
        package_document: EpubPackageDocument,
        epub_configuration: EpubPackageConfiguration,
        source_file_path: str,
        content_file_count: int) -> None:

    file_name = document_operations.generate_section_file_name("Information.xhtml", -1, content_file_count)

    destination_file_path = os.path.join("Content", convert_helpers.sanitize_for_file_name_and_href(file_name))

    reference = destination_file_path
    identifier = convert_helpers.sanitize_for_identifier(reference)
    media_type = epub_xhtml_helpers.get_media_type(reference)

    package_document.add_manifest_item(EpubManifestItem(identifier, reference, media_type))
    package_document.add_spine_item(EpubSpineItem(identifier))

    epub_configuration.content_file_mappings.append((source_file_path, destination_file_path))



def add_content_files(
        package_document: EpubPackageDocument,
        epub_configuration: EpubPackageConfiguration,
        content_file_collection: List[str]) -> None:

    file_count = len(content_file_collection)

    for file_index, source_file_path in enumerate(content_file_collection):
        file_name = re.sub(r"^[0-9]+ - ", "", os.path.basename(source_file_path))
        file_name = document_operations.generate_section_file_name(file_name, file_index, file_count)

        destination_file_path = os.path.join("Content", convert_helpers.sanitize_for_file_name_and_href(file_name))

        reference = destination_file_path
        identifier = convert_helpers.sanitize_for_identifier(reference)
        media_type = epub_xhtml_helpers.get_media_type(reference)

        package_document.add_manifest_item(EpubManifestItem(identifier, reference, media_type))
        package_document.add_spine_item(EpubSpineItem(identifier))

        epub_configuration.content_file_mappings.append((source_file_path, destination_file_path))


def add_resource_files(
        package_document: EpubPackageDocument,
        epub_configuration: EpubPackageConfiguration,
        resource_file_collection: List[str]) -> None:

    for source_file_path in resource_file_collection:
        destination_file_path = os.path.join("Resources", convert_helpers.sanitize_for_file_name_and_href(os.path.basename(source_file_path)))

        reference = destination_file_path
        identifier = convert_helpers.sanitize_for_identifier(reference)
        media_type = epub_xhtml_helpers.get_media_type(reference)

        package_document.add_manifest_item(EpubManifestItem(identifier, reference, media_type))

        epub_configuration.content_file_mappings.append((source_file_path, destination_file_path))


def add_navigation(
        package_document: EpubPackageDocument,
        epub_configuration: EpubPackageConfiguration,
        landmark_collection: List[dict]) -> None:

    content_file_mapping_collection = [ x for x in epub_configuration.content_file_mappings if os.path.dirname(x[1]) == "Content" ]

    for source_file_path, destination_file_path in content_file_mapping_collection:
        reference = urllib.parse.quote(destination_file_path.replace("\\", "/"))
        xhtml_document = epub_xhtml_helpers.load_xhtml(source_file_path)
        display_name = epub_xhtml_helpers.get_xhtml_title(xhtml_document)

        navigation_item = EpubNavigationItem(
            reference = reference,
            display_name = display_name)

        epub_configuration.navigation_items.append(navigation_item)

    for landmark_as_dict in landmark_collection:
        landmark = EpubLandmark(
            epub_type = landmark_as_dict["type"],
            reference = resolve_navigation_reference(landmark_as_dict["reference"], content_file_mapping_collection),
            display_name = landmark_as_dict["display_name"])

        epub_configuration.landmarks.append(landmark)

    package_document.add_manifest_item(EpubManifestItem("toc_xhtml", "toc.xhtml", "application/xhtml+xml", [ "nav" ]))


def resolve_navigation_reference(reference: str, content_file_mapping_collection: List[Tuple[str,str]]) -> str:
    for source_file_path, destination_file_path in content_file_mapping_collection:
        if os.path.basename(source_file_path) == reference:
            return destination_file_path.replace("\\", "/")

    raise ValueError("Reference not found in file collection")
