# cspell:words dcterms fodt idref itemref oebps opendocument relators rootfile rootfiles

import os

from benjaminhamon_document_manipulation_scripts.generate_epub_files import create_serializer
from benjaminhamon_document_manipulation_scripts.generate_epub_files import generate_epub_files
from benjaminhamon_document_manipulation_toolkit.serialization.yaml_serializer import YamlSerializer


def test_generate_epub_files(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "EpubConfiguration.yaml")
    output_directory = os.path.join(workspace_directory, "EpubFiles")

    _setup_workspace(workspace_directory)

    serializer: YamlSerializer = create_serializer("yaml") # type: ignore
    serializer.max_width = 1000 # To avoid long paths getting split onto multiple lines

    generate_epub_files(
        serializer = serializer,
        configuration_file_path = configuration_file_path,
        destination_directory = output_directory,
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_generate_epub_files_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "EpubConfiguration.yaml")
    output_directory = os.path.join(workspace_directory, "EpubFiles")

    _setup_workspace(workspace_directory)

    serializer: YamlSerializer = create_serializer("yaml") # type: ignore
    serializer.max_width = 1000 # To avoid long paths getting split onto multiple lines

    generate_epub_files(
        serializer = serializer,
        configuration_file_path = configuration_file_path,
        destination_directory = output_directory,
        simulate = True,
    )

    assert not os.path.exists(output_directory)


def _setup_workspace(workspace_directory: str) -> None:

    def create_configuration() -> None:
        configuration_file_path = os.path.join(workspace_directory, "EpubConfiguration.yaml")

        configuration_data = """
metadata:
  - key: dc:identifier
    value: urn:isbn:0000000000000
    xhtml_identifier: metadata-identifier

  - key: dc:title
    value: Some Title

  - key: dc:language
    value: en-US

  - key: dc:creator
    value: Some Author
    xhtml_identifier: metadata-author
    refines:
      - property: role
        scheme: marc:relators
        value: aut
      - property: file-as
        value: Author, Some

content_files:
  - "{workspace_directory}/SectionsAsXhtml/*.xhtml"

resource_files:
  - "{workspace_directory}/Styles.css"
"""

        configuration_data = configuration_data.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        os.makedirs(workspace_directory)
        with open(configuration_file_path, mode = "w", encoding = "utf-8") as configuration_file:
            configuration_file.write(configuration_data)

    def create_xhtml() -> None:
        os.makedirs(os.path.join(workspace_directory, "SectionsAsXhtml"))

        for chapter_number in [ 1, 2, 3 ]:
            xhtml_file_path = os.path.join(workspace_directory, "SectionsAsXhtml",
                "{chapter_number} - Chapter {chapter_number}.xhtml".format(chapter_number = chapter_number))

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

    create_configuration()
    create_xhtml()
    create_css()


def _assert_output(workspace_directory: str) -> None: # pylint: disable = too-many-locals
    output_directory = os.path.join(workspace_directory, "EpubFiles")

    files_in_destination = os.listdir(output_directory)
    files_in_destination_expected = [ "container.xml", "content.opf", "content.yaml", "toc.xhtml" ]

    assert files_in_destination == files_in_destination_expected

    def assert_content_configuration() -> None:
        content_configuration_file_path = os.path.join(output_directory, "content.yaml")
        with open(content_configuration_file_path, mode = "r", encoding = "utf-8") as content_configuration_file:
            content_configuration_data = content_configuration_file.read()

        content_configuration_data_expected = """
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

        content_configuration_data_expected = content_configuration_data_expected.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        assert content_configuration_data == content_configuration_data_expected

    def assert_container() -> None:
        container_file_path = os.path.join(output_directory, "container.xml")
        with open(container_file_path, mode = "r", encoding = "utf-8") as container_file:
            container_data = container_file.read()

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
        opf_file_path = os.path.join(output_directory, "content.opf")
        with open(opf_file_path, mode = "r", encoding = "utf-8") as opf_file:
            opf_data = opf_file.read()

        opf_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="metadata-identifier">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="metadata-identifier">urn:isbn:0000000000000</dc:identifier>
    <dc:title>Some Title</dc:title>
    <dc:language>en-US</dc:language>
    <dc:creator id="metadata-author">Some Author</dc:creator>
    <meta refines="#metadata-author" property="role" scheme="marc:relators">aut</meta>
    <meta refines="#metadata-author" property="file-as">Author, Some</meta>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="toc" href="toc.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="1___Chapter_1_xhtml" href="Content/1_-_Chapter_1.xhtml" media-type="application/xhtml+xml"/>
    <item id="2___Chapter_2_xhtml" href="Content/2_-_Chapter_2.xhtml" media-type="application/xhtml+xml"/>
    <item id="3___Chapter_3_xhtml" href="Content/3_-_Chapter_3.xhtml" media-type="application/xhtml+xml"/>
    <item id="Styles_css" href="Resources/Styles.css" media-type="text/css"/>
  </manifest>
  <spine>
    <itemref idref="1___Chapter_1_xhtml" linear="yes"/>
    <itemref idref="2___Chapter_2_xhtml" linear="yes"/>
    <itemref idref="3___Chapter_3_xhtml" linear="yes"/>
  </spine>
</package>
"""

        opf_data_expected = opf_data_expected.lstrip()

        assert opf_data == opf_data_expected

    def assert_navigation() -> None:
        toc_file_path = os.path.join(output_directory, "toc.xhtml")
        with open(toc_file_path, mode = "r", encoding = "utf-8") as toc_file:
            toc_data = toc_file.read()

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

        toc_data_expected = toc_data_expected.lstrip()

        assert toc_data == toc_data_expected

    assert_content_configuration()
    assert_container()
    assert_package_document()
    assert_navigation()
