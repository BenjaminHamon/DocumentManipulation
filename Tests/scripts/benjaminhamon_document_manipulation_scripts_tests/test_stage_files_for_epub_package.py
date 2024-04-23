# cspell:words dcterms fodt idref itemref oebps opendocument relators rootfile rootfiles

import datetime
import glob
import os

from benjaminhamon_document_manipulation_scripts.stage_files_for_epub_package import create_serializer
from benjaminhamon_document_manipulation_scripts.stage_files_for_epub_package import stage_files_for_epub_package


def test_stage_files_for_epub_package(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "EpubFiles", "configuration.yaml")
    output_directory = os.path.join(workspace_directory, "Staging")

    _setup_workspace(workspace_directory)

    stage_files_for_epub_package(
        serializer = create_serializer("yaml"),
        configuration_file_path = configuration_file_path,
        destination_directory = output_directory,
        modified = datetime.datetime(2020, 1, 1, tzinfo = datetime.timezone.utc),
        parameters = {},
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_stage_files_for_epub_package_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "EpubFiles", "configuration.yaml")
    output_directory = os.path.join(workspace_directory, "Staging")

    _setup_workspace(workspace_directory)

    stage_files_for_epub_package(
        serializer = create_serializer("yaml"),
        configuration_file_path = configuration_file_path,
        destination_directory = output_directory,
        modified = datetime.datetime(2020, 1, 1, tzinfo = datetime.timezone.utc),
        parameters = {},
        simulate = True,
    )

    assert not os.path.exists(output_directory)


def _setup_workspace(workspace_directory: str) -> None:

    def create_configuration() -> None:
        configuration_file_path = os.path.join(workspace_directory, "EpubFiles", "configuration.yaml")

        configuration_data = """
file_mappings:
  - - {workspace_directory}/EpubFiles/content.opf
    - EPUB/content.opf
  - - {workspace_directory}/EpubFiles/toc.xhtml
    - EPUB/toc.xhtml
  - - {workspace_directory}/EpubFiles/container.xml
    - META-INF/container.xml
  - - {workspace_directory}/SectionsAsXhtml/1 - Chapter 1.xhtml
    - EPUB/Content/1_-_Chapter_1.xhtml
  - - {workspace_directory}/SectionsAsXhtml/2 - Chapter 2.xhtml
    - EPUB/Content/2_-_Chapter_2.xhtml
  - - {workspace_directory}/SectionsAsXhtml/3 - Chapter 3.xhtml
    - EPUB/Content/3_-_Chapter_3.xhtml
  - - {workspace_directory}/Styles.css
    - EPUB/Resources/Styles.css

link_mappings:
  - - {workspace_directory}/Styles.css
    - EPUB/Resources/Styles.css
"""

        configuration_data = configuration_data.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        with open(configuration_file_path, mode = "w", encoding = "utf-8") as configuration_file:
            configuration_file.write(configuration_data)

    def create_container() -> None:
        container_file_path = os.path.join(workspace_directory, "EpubFiles", "container.xml")

        container_data = """
<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

        container_data = container_data.lstrip()

        with open(container_file_path, mode = "w", encoding = "utf-8") as container_file:
            container_file.write(container_data)

    def create_package_document() -> None:
        opf_file_path = os.path.join(workspace_directory, "EpubFiles", "content.opf")

        opf_data = """
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Some Title</dc:title>
    <dc:language>en-US</dc:language>
    <dc:creator id="metadata-author">Some Author</dc:creator>
    <meta refines="#metadata-author" property="role" scheme="marc:relators">aut</meta>
    <meta refines="#metadata-author" property="file-as">Author, Some</meta>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="EPUB_Content_1___Chapter_1_xhtml" href="Content/1_-_Chapter_1.xhtml" media-type="application/xhtml+xml"/>
    <item id="EPUB_Content_2___Chapter_2_xhtml" href="Content/2_-_Chapter_2.xhtml" media-type="application/xhtml+xml"/>
    <item id="EPUB_Content_3___Chapter_3_xhtml" href="Content/3_-_Chapter_3.xhtml" media-type="application/xhtml+xml"/>
    <item id="EPUB_Resources_Styles_css" href="Resources/Styles.css" media-type="text/css"/>
    <item id="toc_xhtml" href="../toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>
    <itemref idref="EPUB_Content_1___Chapter_1_xhtml" linear="yes"/>
    <itemref idref="EPUB_Content_2___Chapter_2_xhtml" linear="yes"/>
    <itemref idref="EPUB_Content_3___Chapter_3_xhtml" linear="yes"/>
  </spine>
</package>
"""

        opf_data = opf_data.lstrip()

        with open(opf_file_path, mode = "w", encoding = "utf-8") as opf_file:
            opf_file.write(opf_data)

    def create_navigation() -> None:
        toc_file_path = os.path.join(workspace_directory, "EpubFiles", "toc.xhtml")

        toc_data = """
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
          <a href="Content/1_-_Chapter_1.xhtml">Chapter 1</a>
        </li>
        <li>
          <a href="Content/2_-_Chapter_2.xhtml">Chapter 2</a>
        </li>
        <li>
          <a href="Content/3_-_Chapter_3.xhtml">Chapter 3</a>
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

        toc_data = toc_data.lstrip()

        with open(toc_file_path, mode = "w", encoding = "utf-8") as toc_file:
            toc_file.write(toc_data)

    def create_xhtml() -> None:
        for chapter_number in [ 1, 2, 3 ]:
            xhtml_file_path = os.path.join(
                workspace_directory, "SectionsAsXhtml", "{chapter_number} - Chapter {chapter_number}.xhtml".format(chapter_number = chapter_number))

            xhtml_data = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Chapter {chapter_number}</title>
    <link href="../Styles.css" rel="stylesheet" type="text/css"/>
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

            xhtml_data = xhtml_data.lstrip().format(chapter_number = chapter_number)

            with open(xhtml_file_path, mode = "w", encoding = "utf-8") as xhtml_file:
                xhtml_file.write(xhtml_data)

    def create_css() -> None:
        css_file_path = os.path.join(workspace_directory, "Styles.css")
        with open(css_file_path, mode = "w", encoding = "utf-8") as css_file:
            css_file.write("")

    os.makedirs(workspace_directory)
    os.makedirs(os.path.join(workspace_directory, "EpubFiles"))
    os.makedirs(os.path.join(workspace_directory, "SectionsAsXhtml"))

    create_configuration()
    create_container()
    create_package_document()
    create_navigation()
    create_xhtml()
    create_css()


def _assert_output(workspace_directory: str) -> None:

    def assert_file_collection() -> None:
        output_directory = os.path.join(workspace_directory, "Staging")

        files_in_destination = glob.glob(os.path.join(output_directory, "**"), recursive = True)
        files_in_destination = [ os.path.relpath(path, output_directory) for path in files_in_destination if os.path.isfile(path) ]
        files_in_destination.sort()

        files_in_destination_expected = [
            os.path.join("EPUB", "Content", "1_-_Chapter_1.xhtml"),
            os.path.join("EPUB", "Content", "2_-_Chapter_2.xhtml"),
            os.path.join("EPUB", "Content", "3_-_Chapter_3.xhtml"),
            os.path.join("EPUB", "Resources", "Styles.css"),
            os.path.join("EPUB", "content.opf"),
            os.path.join("EPUB", "toc.xhtml"),
            os.path.join("META-INF", "container.xml"),
        ]

        files_in_destination_expected.sort()

        assert files_in_destination == files_in_destination_expected

    def assert_package_document() -> None:
        opf_file_path = os.path.join(workspace_directory, "Staging", "EPUB", "content.opf")

        with open(opf_file_path, mode = "r", encoding = "utf-8") as opf_file:
            opf_data = opf_file.read()

        opf_data_expected ="""
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Some Title</dc:title>
    <dc:language>en-US</dc:language>
    <dc:creator id="metadata-author">Some Author</dc:creator>
    <meta refines="#metadata-author" property="role" scheme="marc:relators">aut</meta>
    <meta refines="#metadata-author" property="file-as">Author, Some</meta>
    <meta property="dcterms:modified">2020-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="EPUB_Content_1___Chapter_1_xhtml" href="Content/1_-_Chapter_1.xhtml" media-type="application/xhtml+xml"/>
    <item id="EPUB_Content_2___Chapter_2_xhtml" href="Content/2_-_Chapter_2.xhtml" media-type="application/xhtml+xml"/>
    <item id="EPUB_Content_3___Chapter_3_xhtml" href="Content/3_-_Chapter_3.xhtml" media-type="application/xhtml+xml"/>
    <item id="EPUB_Resources_Styles_css" href="Resources/Styles.css" media-type="text/css"/>
    <item id="toc_xhtml" href="../toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
  </manifest>
  <spine>
    <itemref idref="EPUB_Content_1___Chapter_1_xhtml" linear="yes"/>
    <itemref idref="EPUB_Content_2___Chapter_2_xhtml" linear="yes"/>
    <itemref idref="EPUB_Content_3___Chapter_3_xhtml" linear="yes"/>
  </spine>
</package>
"""

        opf_data_expected = opf_data_expected.lstrip()

        assert opf_data == opf_data_expected

    def assert_xhtml_files() -> None:
        for chapter_number in [ 1, 2, 3 ]:
            xhtml_file_path = os.path.join(workspace_directory, "Staging", "EPUB", "Content",
                "{chapter_number}_-_Chapter_{chapter_number}.xhtml".format(chapter_number = chapter_number))

            with open(xhtml_file_path, mode = "r", encoding = "utf-8") as xhtml_file:
                xhtml_data = xhtml_file.read()

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

    assert_file_collection()
    assert_package_document()
    assert_xhtml_files()
