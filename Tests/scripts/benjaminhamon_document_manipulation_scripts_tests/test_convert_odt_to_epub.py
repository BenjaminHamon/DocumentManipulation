# cspell:words dcterms fodt idref itemref oebps opendocument rootfile rootfiles

import datetime
import io
import os
import zipfile

import pytest

from benjaminhamon_document_manipulation_scripts.convert_odt_to_epub import convert_odt_to_epub


def test_convert_odt_to_epub(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToEpubConfiguration.yaml")
    definition_file_path = os.path.join(workspace_directory, "DocumentDefinition.yaml")
    intermediate_directory = os.path.join(workspace_directory, "Intermediate")
    package_file_path = os.path.join(workspace_directory, "Document.epub")

    _setup_workspace(workspace_directory)

    convert_odt_to_epub(
        configuration_file_path = configuration_file_path,
        definition_file_path = definition_file_path,
        source_file_path = None,
        destination_file_path = package_file_path,
        intermediate_directory = intermediate_directory,
        now = datetime.datetime(2020, 1, 1, tzinfo = datetime.timezone.utc),
        extra_information = {},
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_convert_odt_to_epub_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToEpubConfiguration.yaml")
    definition_file_path = os.path.join(workspace_directory, "DocumentDefinition.yaml")
    intermediate_directory = os.path.join(workspace_directory, "Intermediate")
    package_file_path = os.path.join(workspace_directory, "Document.epub")

    _setup_workspace(workspace_directory)

    with pytest.raises(NotImplementedError):
        convert_odt_to_epub(
            configuration_file_path = configuration_file_path,
            definition_file_path = definition_file_path,
            source_file_path = None,
            destination_file_path = package_file_path,
            intermediate_directory = intermediate_directory,
            now = datetime.datetime(2020, 1, 1, tzinfo = datetime.timezone.utc),
            extra_information = {},
            simulate = True,
        )

    assert not os.path.exists(intermediate_directory)
    assert not os.path.exists(package_file_path)


def _setup_workspace(workspace_directory: str) -> None:

    def create_configuration() -> None:
        configuration_file_path = os.path.join(workspace_directory, "OdtToEpubConfiguration.yaml")

        configuration_data = """
xhtml_information_template_file_path: "{workspace_directory}/InformationTemplate.xhtml"
source_section_regex: "^Chapter "
style_sheet_file_path: "{workspace_directory}/Styles.css"
resource_files: [ "{workspace_directory}/Styles.css" ]
"""

        configuration_data = configuration_data.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        with open(configuration_file_path, mode = "w", encoding = "utf-8") as configuration_file:
            configuration_file.write(configuration_data)

    def create_definition() -> None:
        definition_file_path = os.path.join(workspace_directory, "DocumentDefinition.yaml")

        definition_data = """
information_file_path: "{workspace_directory}/Information.yaml"
source_file_path: "{workspace_directory}/FullText.fodt"
content_section_identifiers: [ "Chapter *" ]
"""

        definition_data = definition_data.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        with open(definition_file_path, mode = "w", encoding = "utf-8") as definition_file:
            definition_file.write(definition_data)

    def create_information() -> None:
        information_file_path = os.path.join(workspace_directory, "Information.yaml")

        information_data = """
identifier: "ISBN 000-0-0000000-0-0"
language: "en-US"
title: "Some Title"
author: "Some Author"
publisher: "Some Publisher"
copyright: "Copyright © 2020 Some Author"
version_identifier: "1.0.0"
"""

        information_data = information_data.lstrip()

        with open(information_file_path, mode = "w", encoding = "utf-8") as information_file:
            information_file.write(information_data)

    def create_fodt() -> None:
        fodt_file_path = os.path.join(workspace_directory, "FullText.fodt")

        fodt_data = """
<?xml version="1.0" encoding="utf-8"?>
<office:document
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:meta>
    <meta:user-defined meta:name="Language">English</meta:user-defined>
  </office:meta>
  <office:body>
    <office:text>
      <text:h text:style-name="section-heading">Foreword</text:h>
      <text:p text:style-name="section-paragraph">Foreword text</text:p>
      <text:h text:style-name="section-heading">Chapter 1</text:h>
      <text:p text:style-name="section-paragraph">Chapter 1 paragraph 1</text:p>
      <text:p text:style-name="section-paragraph">Chapter 1 paragraph 2</text:p>
      <text:p text:style-name="section-paragraph">Chapter 1 paragraph 3</text:p>
      <text:h text:style-name="section-heading">Chapter 2</text:h>
      <text:p text:style-name="section-paragraph">Chapter 2 paragraph 1</text:p>
      <text:p text:style-name="section-paragraph">Chapter 2 paragraph 2</text:p>
      <text:p text:style-name="section-paragraph">Chapter 2 paragraph 3</text:p>
      <text:h text:style-name="section-heading">Chapter 3</text:h>
      <text:p text:style-name="section-paragraph">Chapter 3 paragraph 1</text:p>
      <text:p text:style-name="section-paragraph">Chapter 3 paragraph 2</text:p>
      <text:p text:style-name="section-paragraph">Chapter 3 paragraph 3</text:p>
    </office:text>
  </office:body>
</office:document>
"""

        fodt_data = fodt_data.lstrip()

        with open(fodt_file_path, mode = "w", encoding = "utf-8") as fodt_file:
            fodt_file.write(fodt_data)

    def create_css() -> None:
        css_file_path = os.path.join(workspace_directory, "Styles.css")
        with open(css_file_path, mode = "w", encoding = "utf-8") as css_file:
            css_file.write("")

    def create_information_template() -> None:
        template_file_path = os.path.join(workspace_directory, "InformationTemplate.xhtml")

        template_data = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Information</title>
  </head>
  <body>
    <section id="book-information">
      <div id="title-information">
        <div class="book-title">{title}</div>
        <div class="book-author">written by {author}</div>
      </div>
      <div id="edition-information">
        <div>Draft {date}</div>
      </div>
      <div id="version-information">
        <div>Version {version_identifier}</div>
      </div>
      <div id="copyright-notice">
        <div>{copyright}</div>
        <div>All rights reserved</div>
      </div>
    </section>
  </body>
</html>
"""

        template_data = template_data.lstrip()

        with open(template_file_path, mode = "w", encoding = "utf-8") as template_file:
            template_file.write(template_data)

    os.makedirs(workspace_directory)
    os.makedirs(os.path.join(workspace_directory, "SectionsAsXhtml"))

    create_configuration()
    create_definition()
    create_information()
    create_fodt()
    create_css()
    create_information_template()


def _assert_output(workspace_directory: str) -> None: # pylint: disable = too-many-statements
    intermediate_directory = os.path.join(workspace_directory, "Intermediate")
    package_file_path = os.path.join(workspace_directory, "Document.epub")

    def assert_archive() -> None:
        assert os.path.exists(package_file_path)

        file_collection_expected = [
            "EPUB/Content/1_-_Information.xhtml",
            "EPUB/Content/2_-_Chapter_1.xhtml",
            "EPUB/Content/3_-_Chapter_2.xhtml",
            "EPUB/Content/4_-_Chapter_3.xhtml",
            "EPUB/Resources/Styles.css",
            "EPUB/content.opf",
            "EPUB/toc.xhtml",
            "META-INF/container.xml",
            "mimetype",
        ]

        file_collection_expected.sort()

        with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
            assert package_file.testzip() is None

            file_collection = [ x.filename for x in package_file.filelist ]
            file_collection.sort()

            assert file_collection == file_collection_expected

            mimetype_data = package_file.read("mimetype").decode("utf-8")

            assert mimetype_data == "application/epub+zip"

    def assert_container() -> None:
        container_file_path = "META-INF/container.xml"
        with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
            with package_file.open(container_file_path, mode = "r") as container_file:
                with io.TextIOWrapper(container_file, encoding = "utf-8") as container_text_file:
                    container_data = container_text_file.read()

        container_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

        container_data_expected = container_data_expected.lstrip()

        assert container_data == container_data_expected

    def assert_package_document() -> None:
        opf_file_path = "EPUB/content.opf"
        with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
            with package_file.open(opf_file_path, mode = "r") as opf_file:
                with io.TextIOWrapper(opf_file, encoding = "utf-8") as opf_text_file:
                    opf_data = opf_text_file.read()

        opf_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="metadata-identifier">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="metadata-identifier">urn:isbn:0000000000000</dc:identifier>
    <dc:title>Some Title</dc:title>
    <dc:language>en-US</dc:language>
    <dc:creator>Some Author</dc:creator>
    <dc:publisher>Some Publisher</dc:publisher>
    <meta property="dcterms:modified">2020-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="1___Information_xhtml" href="Content/1_-_Information.xhtml" media-type="application/xhtml+xml"/>
    <item id="2___Chapter_1_xhtml" href="Content/2_-_Chapter_1.xhtml" media-type="application/xhtml+xml"/>
    <item id="3___Chapter_2_xhtml" href="Content/3_-_Chapter_2.xhtml" media-type="application/xhtml+xml"/>
    <item id="4___Chapter_3_xhtml" href="Content/4_-_Chapter_3.xhtml" media-type="application/xhtml+xml"/>
    <item id="Styles_css" href="Resources/Styles.css" media-type="text/css"/>
  </manifest>
  <spine>
    <itemref idref="1___Information_xhtml" linear="yes"/>
    <itemref idref="2___Chapter_1_xhtml" linear="yes"/>
    <itemref idref="3___Chapter_2_xhtml" linear="yes"/>
    <itemref idref="4___Chapter_3_xhtml" linear="yes"/>
  </spine>
</package>
"""

        opf_data_expected = opf_data_expected.lstrip()

        assert opf_data == opf_data_expected

    def assert_navigation() -> None:
        toc_file_path = "EPUB/toc.xhtml"
        with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
            with package_file.open(toc_file_path, mode = "r") as toc_file:
                with io.TextIOWrapper(toc_file, encoding = "utf-8") as toc_text_file:
                    toc_data = toc_text_file.read()

        toc_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Table of Contents</title>
  </head>
  <body>
    <nav epub:type="toc">
      <h1>Table of Contents</h1>
      <ol>
        <li>
          <a href="Content/1_-_Information.xhtml">Information</a>
        </li>
        <li>
          <a href="Content/2_-_Chapter_1.xhtml">Chapter 1</a>
        </li>
        <li>
          <a href="Content/3_-_Chapter_2.xhtml">Chapter 2</a>
        </li>
        <li>
          <a href="Content/4_-_Chapter_3.xhtml">Chapter 3</a>
        </li>
      </ol>
    </nav>
    <nav epub:type="landmarks">
      <h1>Landmarks</h1>
      <ol/>
    </nav>
  </body>
</html>
"""

        toc_data_expected = toc_data_expected.lstrip()

        assert toc_data == toc_data_expected

    def assert_xhtml() -> None:
        xhtml_file_path = "EPUB/Content/1_-_Information.xhtml"
        with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
            with package_file.open(xhtml_file_path, mode = "r") as xhtml_file:
                with io.TextIOWrapper(xhtml_file, encoding = "utf-8") as xhtml_text_file:
                    xhtml_data = xhtml_text_file.read()

        xhtml_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Information</title>
  </head>
  <body>
    <section id="book-information">
      <div id="title-information">
        <div class="book-title">Some Title</div>
        <div class="book-author">written by Some Author</div>
      </div>
      <div id="edition-information">
        <div>Draft 01-Jan-2020</div>
      </div>
      <div id="version-information">
        <div>Version 1.0.0</div>
      </div>
      <div id="copyright-notice">
        <div>Copyright © 2020 Some Author</div>
        <div>All rights reserved</div>
      </div>
    </section>
  </body>
</html>
"""

        xhtml_data_expected = xhtml_data_expected.lstrip()

        assert xhtml_data == xhtml_data_expected

        for chapter_number in [ 1, 2, 3 ]:
            xhtml_file_path = "EPUB/Content/{index}_-_Chapter_{chapter_number}.xhtml".format(index = chapter_number + 1, chapter_number = chapter_number)
            with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
                with package_file.open(xhtml_file_path, mode = "r") as xhtml_file:
                    with io.TextIOWrapper(xhtml_file, encoding = "utf-8") as xhtml_text_file:
                        xhtml_data = xhtml_text_file.read()

            xhtml_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Chapter {chapter_number}</title>
    <link href="../Resources/Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <section>
      <h1 class="section-heading">
        <span>Chapter {chapter_number}</span>
      </h1>
      <p class="section-paragraph">
        <span>Chapter {chapter_number} paragraph 1</span>
      </p>
      <p class="section-paragraph">
        <span>Chapter {chapter_number} paragraph 2</span>
      </p>
      <p class="section-paragraph">
        <span>Chapter {chapter_number} paragraph 3</span>
      </p>
    </section>
  </body>
</html>
"""

            xhtml_data_expected = xhtml_data_expected.lstrip().format(chapter_number = chapter_number)

            assert xhtml_data == xhtml_data_expected

    assert os.path.exists(intermediate_directory)

    assert_archive()
    assert_container()
    assert_package_document()
    assert_navigation()
    assert_xhtml()
