""" Unit tests for EpubPackageBuilder """

import os
import zipfile

from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation import EpubNavigation
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_builder import EpubPackageBuilder
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_document import EpubPackageDocument


def test_update_xhtml_links(tmpdir):
    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    staging_directory = os.path.join(tmpdir, "Working")

    os.makedirs(staging_directory)

    xhtml_file_content_initial = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <link href="https://www.example.com/Styles/Examples.css" rel="stylesheet" type="text/css"/>
    <link href="../Styles/Generic.css" rel="stylesheet" type="text/css"/>
    <link href="../Styles/LocalEnvironment.css" rel="stylesheet" type="text/css"/>
  </head>
  <body/>
</html>
"""

    os.makedirs(os.path.join(staging_directory, "EPUB", "content"))
    with open(os.path.join(staging_directory, "EPUB", "content", "file.xhtml"), mode = "w", encoding = "utf-8") as xhtml_file:
        xhtml_file.write(xhtml_file_content_initial.lstrip())

    package_builder.update_xhtml_links(
        staging_directory = staging_directory,
        content_files = [
            ("Sources/Xhtml/File.xhtml", "EPUB/Content/File.xhtml") ],
        link_mappings = [
            ("https://www.example.com/Styles/Examples.css", "https://www.example.com/Styles/ExamplesModified.css"),
            ("Sources/Styles/Generic.css", "EPUB/Resources/Generic.css"),
            ("Sources/Styles/LocalEnvironment.css", "EPUB/Resources/TargetEnvironment.css") ])

    with open(os.path.join(staging_directory, "EPUB", "content", "file.xhtml"), mode = "r", encoding = "utf-8") as xhtml_file:
        xhtml_file_content_final = xhtml_file.read()

    xhtml_file_content_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <link href="https://www.example.com/Styles/ExamplesModified.css" rel="stylesheet" type="text/css"/>
    <link href="../Resources/Generic.css" rel="stylesheet" type="text/css"/>
    <link href="../Resources/TargetEnvironment.css" rel="stylesheet" type="text/css"/>
  </head>
  <body/>
</html>
"""

    xhtml_file_content_expected = xhtml_file_content_expected.lstrip()

    assert xhtml_file_content_final == xhtml_file_content_expected


def test_create_package(tmpdir):
    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    source_directory = os.path.join(tmpdir, "Sources")
    staging_directory = os.path.join(tmpdir, "Working")
    package_file_path = os.path.join(tmpdir, "Output", "package.epub")
    container_file_path = os.path.join(source_directory, "container.xml")
    package_document_file_path = os.path.join(source_directory, "content.opf")
    toc_file_path = os.path.join(source_directory, "toc.xhtml")

    os.makedirs(source_directory)
    content_writer.write_xml(os.path.join(source_directory, "my_first_section.xhtml"), epub_xhtml_helpers.create_xhtml())
    content_writer.write_xml(os.path.join(source_directory, "my_second_section.xhtml"), epub_xhtml_helpers.create_xhtml())
    container_file_path = os.path.join(source_directory, "container.xml")
    package_document_file_path = os.path.join(source_directory, "content.opf")
    toc_file_path = os.path.join(source_directory, "toc.xhtml")

    package_document = EpubPackageDocument()
    epub_content_configuration = EpubContentConfiguration()
    epub_navigation = EpubNavigation(
        [ EpubNavigationItem("my_first_section.xhtml", "first section"), EpubNavigationItem("my_second_section.xhtml", "second section") ], [])

    content_writer.write_package_document_file(package_document_file_path, package_document, "EPUB")
    content_writer.write_navigation_file(toc_file_path, epub_navigation, "EPUB")
    content_writer.write_container_file(container_file_path, os.path.join("EPUB", "content.opf"))

    epub_content_configuration.file_mappings = [
        (container_file_path, os.path.join("META-INF", "container.xml")),
        (package_document_file_path, os.path.join("EPUB", "content.opf")),
        (os.path.join(source_directory, "my_first_section.xhtml"), os.path.join("EPUB", "my_first_section.xhtml")),
        (os.path.join(source_directory, "my_second_section.xhtml"),os.path.join("EPUB", "my_second_section.xhtml")),
        (toc_file_path, os.path.join("EPUB", "toc.xhtml")),
    ]

    package_builder.stage_files(staging_directory, epub_content_configuration.file_mappings, simulate = False)
    package_builder.create_package(package_file_path, staging_directory, simulate = False)

    file_collection_expected = [
        "EPUB/content.opf",
        "EPUB/my_first_section.xhtml",
        "EPUB/my_second_section.xhtml",
        "EPUB/toc.xhtml",
        "META-INF/container.xml",
        "mimetype",
    ]

    assert os.path.exists(package_file_path)

    with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
        assert package_file.testzip() is None

        file_collection = [ x.filename for x in package_file.filelist ]
        file_collection.sort()

        assert file_collection == file_collection_expected
