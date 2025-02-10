# cspell:words fodt opendocument

import os

from benjaminhamon_document_manipulation_scripts.rewrite_odt import rewrite_odt


def test_rewrite_odt(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_file_path = os.path.join(workspace_directory, "FullTextRewritten.fodt")

    _setup_workspace(workspace_directory)

    rewrite_odt(
        source_file_path = source_file_path,
        destination_file_path = output_file_path,
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_rewrite_odt_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_file_path = os.path.join(workspace_directory, "FullTextRewritten.fodt")

    _setup_workspace(workspace_directory)

    rewrite_odt(
        source_file_path = source_file_path,
        destination_file_path = output_file_path,
        simulate = True,
    )

    assert not os.path.exists(output_file_path)


def _setup_workspace(workspace_directory: str) -> None:
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")

    fodt_data = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
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


def _assert_output(workspace_directory: str) -> None:
    output_file_path = os.path.join(workspace_directory, "FullTextRewritten.fodt")

    assert os.path.exists(output_file_path)

    with open(output_file_path, mode = "r", encoding = "utf-8") as output_file:
        fodt_data = output_file.read()

    fodt_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h text:style-name="section-heading"><text:span>Foreword</text:span></text:h>
      <text:p text:style-name="section-paragraph"><text:span>Foreword text</text:span></text:p>
      <text:h text:style-name="section-heading"><text:span>Chapter 1</text:span></text:h>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 1 paragraph 1</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 1 paragraph 2</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 1 paragraph 3</text:span></text:p>
      <text:h text:style-name="section-heading"><text:span>Chapter 2</text:span></text:h>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 2 paragraph 1</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 2 paragraph 2</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 2 paragraph 3</text:span></text:p>
      <text:h text:style-name="section-heading"><text:span>Chapter 3</text:span></text:h>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 3 paragraph 1</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 3 paragraph 2</text:span></text:p>
      <text:p text:style-name="section-paragraph"><text:span>Chapter 3 paragraph 3</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    fodt_data_expected = fodt_data_expected.lstrip()

    assert fodt_data == fodt_data_expected
