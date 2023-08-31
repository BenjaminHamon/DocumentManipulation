""" Unit tests for EpubPackageBuilder """

import os
import zipfile
from benjaminhamon_book_distribution_toolkit.epub import epub_xhtml_helpers

from benjaminhamon_book_distribution_toolkit.epub.epub_package_builder import EpubPackageBuilder
from benjaminhamon_book_distribution_toolkit.epub.epub_package_configuration import EpubPackageConfiguration
from benjaminhamon_book_distribution_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_book_distribution_toolkit.epub.epub_package_document import EpubPackageDocument


def test_stage_package_files(tmpdir):
    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    source_directory = os.path.join(tmpdir, "Sources")
    staging_directory = os.path.join(tmpdir, "Working")

    os.makedirs(source_directory)
    content_writer.write_xml(os.path.join(source_directory, "my_first_section.xhtml"), epub_xhtml_helpers.create_xhtml())
    content_writer.write_xml(os.path.join(source_directory, "my_second_section.xhtml"), epub_xhtml_helpers.create_xhtml())

    epub_configuration = EpubPackageConfiguration()

    epub_configuration.content_file_mappings = [
        (os.path.join(source_directory, "my_first_section.xhtml"), "my_first_section.xhtml"),
        (os.path.join(source_directory, "my_second_section.xhtml"), "my_second_section.xhtml"),
    ]

    package_document = EpubPackageDocument()

    package_builder.stage_package_files(staging_directory, epub_configuration, package_document, simulate = False)

    assert os.path.exists(os.path.join(staging_directory, "EPUB", "my_first_section.xhtml"))
    assert os.path.exists(os.path.join(staging_directory, "EPUB", "my_second_section.xhtml"))
    assert os.path.exists(os.path.join(staging_directory, "EPUB", "toc.xhtml"))
    assert os.path.exists(os.path.join(staging_directory, "EPUB", "package.opf"))
    assert os.path.exists(os.path.join(staging_directory, "META-INF", "container.xml"))


def test_stage_package_files_with_simulate(tmpdir):
    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    source_directory = os.path.join(tmpdir, "Sources")
    staging_directory = os.path.join(tmpdir, "Working")

    epub_configuration = EpubPackageConfiguration()

    epub_configuration.content_file_mappings = [
        (os.path.join(source_directory, "my_first_section.xhtml"), "my_first_section.xhtml"),
        (os.path.join(source_directory, "my_second_section.xhtml"), "my_second_section.xhtml"),
    ]

    package_document = EpubPackageDocument()

    package_builder.stage_package_files(staging_directory, epub_configuration, package_document, simulate = True)


def test_update_xhtml_links(tmpdir):
    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    staging_directory = os.path.join(tmpdir, "Working")

    os.makedirs(staging_directory)

    xhtml_file_content_initial = """
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <link href="../styles/default.css" rel="stylesheet" type="text/css"/>
  </head>
  <body/>
</html>
"""

    os.makedirs(os.path.join(staging_directory, "EPUB", "content"))
    with open(os.path.join(staging_directory, "EPUB", "content", "file.xhtml"), mode = "w", encoding = "utf-8") as xhtml_file:
        xhtml_file.write(xhtml_file_content_initial.lstrip())

    package_builder.update_xhtml_links(staging_directory, [ ("content/file.xhtml", "content/file.xhtml") ], [ ("styles/default.css", "styles/final.css") ])

    with open(os.path.join(staging_directory, "EPUB", "content", "file.xhtml"), mode = "r", encoding = "utf-8") as xhtml_file:
        xhtml_file_content_final = xhtml_file.read()

    xhtml_file_content_expected = """
<?xml version='1.0' encoding='UTF-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <link href="../styles/final.css" rel="stylesheet" type="text/css"/>
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

    os.makedirs(source_directory)
    content_writer.write_xml(os.path.join(source_directory, "my_first_section.xhtml"), epub_xhtml_helpers.create_xhtml())
    content_writer.write_xml(os.path.join(source_directory, "my_second_section.xhtml"), epub_xhtml_helpers.create_xhtml())

    epub_configuration = EpubPackageConfiguration()

    epub_configuration.content_file_mappings = [
        (os.path.join(source_directory, "my_first_section.xhtml"), "my_first_section.xhtml"),
        (os.path.join(source_directory, "my_second_section.xhtml"), "my_second_section.xhtml"),
    ]

    package_document = EpubPackageDocument()

    package_builder.stage_package_files(staging_directory, epub_configuration, package_document, simulate = False)
    package_builder.create_package(package_file_path, staging_directory, simulate = False)

    assert os.path.exists(package_file_path)

    with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
        assert package_file.testzip() is None

        file_collection = [ x.filename for x in package_file.filelist ]

        assert "EPUB/my_first_section.xhtml" in file_collection
        assert "EPUB/my_second_section.xhtml" in file_collection
        assert "EPUB/toc.xhtml" in file_collection
        assert "EPUB/package.opf" in file_collection
        assert "META-INF/container.xml" in file_collection
        assert "mimetype" in file_collection
