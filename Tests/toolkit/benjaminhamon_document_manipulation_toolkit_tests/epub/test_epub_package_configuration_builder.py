""" Unit tests for EpubPackageConfigurationBuilder """

# cspell:words bodymatter booleaness

import os
import re
from typing import List, Tuple

from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.epub.epub_manifest_item import EpubManifestItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_configuration_builder import EpubPackageConfigurationBuilder
from benjaminhamon_document_manipulation_toolkit.epub.epub_spine_item import EpubSpineItem


def test_add_main_files():
    builder = EpubPackageConfigurationBuilder()

    builder.add_main_files("EpubFiles")

    configuration = builder.get_configuration()

    file_mappings_expected = [
        (os.path.join("EpubFiles", "content.opf"), os.path.join("EPUB", "content.opf")),
        (os.path.join("EpubFiles", "toc.xhtml"), os.path.join("EPUB", "toc.xhtml")),
        (os.path.join("EpubFiles", "container.xml"), os.path.join("META-INF", "container.xml")),
    ]

    assert configuration.document.get_manifest_items() == [ EpubManifestItem("toc", "EPUB/toc.xhtml", "application/xhtml+xml", [ "nav" ]) ]
    assert configuration.document.get_spine_items() == [] # pylint: disable = use-implicit-booleaness-not-comparison
    assert configuration.content_configuration.file_mappings == file_mappings_expected


def test_add_content_files():

    def get_title(xhtml_file_path: str) -> str:
        match = re.search(r"^(?P<title>.*?)\.xhtml$", os.path.basename(xhtml_file_path))
        if match is None:
            raise ValueError
        return match.group("title")

    builder = EpubPackageConfigurationBuilder()

    content_file_collection = [
        os.path.join("SectionsAsXhtml", "File1.xhtml"),
        os.path.join("SectionsAsXhtml", "File2.xhtml"),
        os.path.join("SectionsAsXhtml", "File3.xhtml"),
    ]

    builder.add_content_files(content_file_collection, get_title)

    configuration = builder.get_configuration()

    manifest_expected = [
        EpubManifestItem("1___File1_xhtml", "EPUB/Content/1_-_File1.xhtml", "application/xhtml+xml"),
        EpubManifestItem("2___File2_xhtml", "EPUB/Content/2_-_File2.xhtml", "application/xhtml+xml"),
        EpubManifestItem("3___File3_xhtml", "EPUB/Content/3_-_File3.xhtml", "application/xhtml+xml"),
    ]

    spine_expected = [
        EpubSpineItem("1___File1_xhtml"),
        EpubSpineItem("2___File2_xhtml"),
        EpubSpineItem("3___File3_xhtml"),
    ]

    file_mappings_expected = [
        (os.path.join("SectionsAsXhtml", "File1.xhtml"), os.path.join("EPUB", "Content", "1_-_File1.xhtml")),
        (os.path.join("SectionsAsXhtml", "File2.xhtml"), os.path.join("EPUB", "Content", "2_-_File2.xhtml")),
        (os.path.join("SectionsAsXhtml", "File3.xhtml"), os.path.join("EPUB", "Content", "3_-_File3.xhtml")),
    ]

    navigation_expected = [
        EpubNavigationItem("EPUB/Content/1_-_File1.xhtml", "File1"),
        EpubNavigationItem("EPUB/Content/2_-_File2.xhtml", "File2"),
        EpubNavigationItem("EPUB/Content/3_-_File3.xhtml", "File3"),
    ]

    assert configuration.document.get_manifest_items() == manifest_expected
    assert configuration.document.get_spine_items() == spine_expected
    assert configuration.content_configuration.file_mappings == file_mappings_expected
    assert configuration.navigation.navigation_items == navigation_expected



def test_add_cover():
    builder = EpubPackageConfigurationBuilder()

    builder.add_cover(os.path.join("Sources", "DocumentCover.jpeg"))

    configuration = builder.get_configuration()

    assert configuration.document.get_manifest_items() == [ EpubManifestItem("cover", "EPUB/cover.jpeg", "image/jpeg", [ "cover-image" ]) ]
    assert configuration.document.get_spine_items() == [] # pylint: disable = use-implicit-booleaness-not-comparison
    assert configuration.content_configuration.file_mappings == [ (os.path.join("Sources", "DocumentCover.jpeg"), os.path.join("EPUB", "cover.jpeg")) ]


def test_add_resource_files():
    builder = EpubPackageConfigurationBuilder()
    resource_file_collection = [ os.path.join("Sources", "Styles.css") ]

    builder.add_resource_files(resource_file_collection)

    configuration = builder.get_configuration()

    assert configuration.document.get_manifest_items() == [ EpubManifestItem("Styles_css", "EPUB/Resources/Styles.css", "text/css") ]
    assert configuration.document.get_spine_items() == [] # pylint: disable = use-implicit-booleaness-not-comparison
    assert configuration.content_configuration.file_mappings == [ (os.path.join("Sources", "Styles.css"), os.path.join("EPUB", "Resources", "Styles.css")) ]
    assert configuration.content_configuration.link_mappings == [ ("Sources/Styles.css", "EPUB/Resources/Styles.css") ]


def test_add_link_overrides():
    builder = EpubPackageConfigurationBuilder()

    builder.get_configuration().content_configuration.link_mappings = [
        ("Sources/Generic.css", "EPUB/Resources/Generic.css"),
        ("Sources/TargetEnvironment.css", "EPUB/Resources/TargetEnvironment.css"),
    ]

    link_override_collection: List[Tuple[str,str]] = [ ("Sources/LocalEnvironment.css", "EPUB/Resources/TargetEnvironment.css") ]

    builder.add_link_overrides(link_override_collection)

    configuration = builder.get_configuration()

    link_mappings_expected = [
        ("Sources/LocalEnvironment.css", "EPUB/Resources/TargetEnvironment.css"),
        ("Sources/Generic.css", "EPUB/Resources/Generic.css"),
        ("Sources/TargetEnvironment.css", "EPUB/Resources/TargetEnvironment.css"),
    ]

    assert configuration.content_configuration.link_mappings == link_mappings_expected


def test_add_landmarks():

    def get_title(xhtml_file_path: str) -> str:
        match = re.search(r"^(?P<title>.*?)\.xhtml$", os.path.basename(xhtml_file_path))
        if match is None:
            raise ValueError
        return match.group("title")

    builder = EpubPackageConfigurationBuilder()

    content_file_collection = [
        os.path.join("SectionsAsXhtml", "Foreword.xhtml"),
        os.path.join("SectionsAsXhtml", "Body.xhtml"),
        os.path.join("SectionsAsXhtml", "Afterword.xhtml"),
    ]

    builder.add_content_files(content_file_collection, get_title)

    builder.add_landmarks([ EpubLandmark("bodymatter", "Body.xhtml", "Body") ])

    configuration = builder.get_configuration()

    assert configuration.navigation.landmarks == [ EpubLandmark("bodymatter", "EPUB/Content/2_-_Body.xhtml", "Body") ]
