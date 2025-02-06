# cspell:words fodt opendocument

import os

from benjaminhamon_document_manipulation_scripts.convert_odt_to_xhtml import convert_odt_to_xhtml
from benjaminhamon_document_manipulation_scripts.convert_odt_to_xhtml import create_serializer


def test_convert_odt_to_xhtml(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    css_file_path = os.path.join(workspace_directory, "Styles.css")
    output_directory = os.path.join(workspace_directory, "SectionsAsXhtml")

    _setup_workspace(workspace_directory)

    convert_odt_to_xhtml(
        serializer = create_serializer("yaml"),
        source_file_path_collection = [ source_file_path ],
        destination_directory = output_directory,
        style_sheet_file_path = css_file_path,
        section_regex = r"^Chapter ",
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_convert_odt_to_xhtml_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    css_file_path = os.path.join(workspace_directory, "Styles.css")
    output_directory = os.path.join(workspace_directory, "SectionsAsXhtml")

    _setup_workspace(workspace_directory)

    convert_odt_to_xhtml(
        serializer = create_serializer("yaml"),
        source_file_path_collection = [ source_file_path ],
        destination_directory = output_directory,
        style_sheet_file_path = css_file_path,
        section_regex = r"^Chapter ",
        simulate = True,
    )

    assert not os.path.exists(output_directory)


def _setup_workspace(workspace_directory: str) -> None:
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    css_file_path = os.path.join(workspace_directory, "Styles.css")

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

    os.makedirs(workspace_directory)
    with open(source_file_path, mode = "w", encoding = "utf-8") as source_file:
        source_file.write(fodt_data)
    with open(css_file_path, mode = "w", encoding = "utf-8") as css_file:
        css_file.write("")


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
