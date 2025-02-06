# cspell:words fodt opendocument

import os

from benjaminhamon_document_manipulation_scripts.split_odt import split_odt


def test_split_odt(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_directory = os.path.join(workspace_directory, "SectionsAsOdt")

    _setup_workspace(workspace_directory)

    split_odt(
        source_file_path = source_file_path,
        destination_directory = output_directory,
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_split_odt_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_directory = os.path.join(workspace_directory, "SectionsAsOdt")

    _setup_workspace(workspace_directory)

    split_odt(
        source_file_path = source_file_path,
        destination_directory = output_directory,
        simulate = True,
    )

    assert not os.path.exists(output_directory)


def _setup_workspace(workspace_directory: str) -> None:
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")

    fodt_data = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
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

    os.makedirs(workspace_directory)
    with open(source_file_path, mode = "w", encoding = "utf-8") as source_file:
        source_file.write(fodt_data)


def _assert_output(workspace_directory: str) -> None:
    output_directory = os.path.join(workspace_directory, "SectionsAsOdt")

    files_in_destination = os.listdir(output_directory)
    files_in_destination_expected = [ "1 - Chapter 1.fodt", "2 - Chapter 2.fodt", "3 - Chapter 3.fodt" ]

    assert files_in_destination == files_in_destination_expected

    for chapter_number in [ 1, 2, 3 ]:
        fodt_file_path = os.path.join(output_directory, "{chapter_number} - Chapter {chapter_number}.fodt".format(chapter_number = chapter_number))
        with open(fodt_file_path, mode = "r", encoding = "utf-8") as fodt_file:
            fodt_data = fodt_file.read()

        fodt_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h text:style-name="section-heading"><text:span>Chapter {chapter_number}</text:span></text:h>
      <text:p text:style-name="section-paragraph"><text:span>Chapter {chapter_number} paragraph 1</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter {chapter_number} paragraph 2</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter {chapter_number} paragraph 3</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

        fodt_data_expected = fodt_data_expected.lstrip().format(chapter_number = chapter_number)

        assert fodt_data == fodt_data_expected
