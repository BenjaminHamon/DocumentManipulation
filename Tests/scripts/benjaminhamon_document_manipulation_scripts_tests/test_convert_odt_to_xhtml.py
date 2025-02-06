# cspell:words fodt opendocument

import os

from benjaminhamon_document_manipulation_scripts.convert_odt_to_xhtml import convert_odt_to_xhtml


def _setup_workspace(workspace_directory: str) -> None:

    def create_configuration() -> None:
        configuration_file_path = os.path.join(workspace_directory, "OdtToXhtmlConfiguration.yaml")

        configuration_data = """
style_sheet_file_path: "{workspace_directory}/Styles.css"
"""

        configuration_data = configuration_data.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        with open(configuration_file_path, mode = "w", encoding = "utf-8") as configuration_file:
            configuration_file.write(configuration_data)


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

    def create_style_sheet() -> None:
        css_file_path = os.path.join(workspace_directory, "Styles.css")

        with open(css_file_path, mode = "w", encoding = "utf-8") as css_file:
            css_file.write("")

    os.makedirs(workspace_directory)

    create_configuration()
    create_fodt()
    create_style_sheet()


def test_convert_odt_to_xhtml_as_many_files(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToXhtmlConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_directory = os.path.join(workspace_directory, "SectionsAsXhtml")

    _setup_workspace(workspace_directory)

    convert_odt_to_xhtml(
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path_or_directory = output_directory,
        write_as_single_file = False,
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_convert_odt_to_xhtml_as_many_files_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToXhtmlConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_directory = os.path.join(workspace_directory, "SectionsAsXhtml")

    _setup_workspace(workspace_directory)

    convert_odt_to_xhtml(
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path_or_directory = output_directory,
        write_as_single_file = False,
        simulate = True,
    )

    assert not os.path.exists(output_directory)


def _assert_output(workspace_directory: str) -> None:
    output_directory = os.path.join(workspace_directory, "SectionsAsXhtml")

    files_in_destination = os.listdir(output_directory)
    files_in_destination_expected = [ "1 - Chapter 1.xhtml", "2 - Chapter 2.xhtml", "3 - Chapter 3.xhtml" ]

    assert files_in_destination == files_in_destination_expected

    for chapter_number in [ 1, 2, 3 ]:
        xhtml_file_path = os.path.join(output_directory, "{chapter_number} - Chapter {chapter_number}.xhtml".format(chapter_number = chapter_number))
        with open(xhtml_file_path, mode = "r", encoding = "utf-8") as xhtml_file:
            xhtml_data = xhtml_file.read()

        xhtml_data_expected = """
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

        xhtml_data_expected = xhtml_data_expected.lstrip().format(chapter_number = chapter_number)

        assert xhtml_data == xhtml_data_expected
