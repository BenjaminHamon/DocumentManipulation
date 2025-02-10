# cspell:words fodt opendocument

import os

from benjaminhamon_document_manipulation_scripts.convert_odt_to_markdown import convert_odt_to_markdown


def _setup_workspace(workspace_directory: str) -> None:

    def create_configuration() -> None:
        configuration_file_path = os.path.join(workspace_directory, "OdtToMarkdownConfiguration.yaml")

        configuration_data = """
extra_metadata:
  identifier: ISBN 000-0-0000000-0-0
  language: en-US
  title: Some Title
  author: Some Author
  publisher: Some Publisher
  copyright: Copyright © 2020 Some Author
  version_identifier: 1.0.0
"""

        configuration_data = configuration_data.lstrip().format(workspace_directory = workspace_directory.replace("\\", "/"))

        with open(configuration_file_path, mode = "w", encoding = "utf-8") as configuration_file:
            configuration_file.write(configuration_data)


    def create_fodt() -> None:
        fodt_file_path = os.path.join(workspace_directory, "FullText.fodt")

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

        with open(fodt_file_path, mode = "w", encoding = "utf-8") as fodt_file:
            fodt_file.write(fodt_data)

    os.makedirs(workspace_directory)

    create_configuration()
    create_fodt()


def test_convert_odt_to_markdown_as_single_document(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToMarkdownConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_file_path = os.path.join(workspace_directory, "FullText.md")

    _setup_workspace(workspace_directory)

    convert_odt_to_markdown(
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path_or_directory = output_file_path,
        write_as_single_file = True,
        simulate = False,
    )

    _assert_output_as_single_document(workspace_directory)


def test_convert_odt_to_markdown_as_single_document_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToMarkdownConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_file_path = os.path.join(workspace_directory, "FullText.md")

    _setup_workspace(workspace_directory)

    convert_odt_to_markdown(
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path_or_directory = output_file_path,
        write_as_single_file = True,
        simulate = True,
    )

    assert not os.path.exists(output_file_path)


def _assert_output_as_single_document(workspace_directory: str) -> None:
    output_file_path = os.path.join(workspace_directory, "FullText.md")
    with open(output_file_path, mode = "r", encoding = "utf-8") as markdown_file:
        markdown_data = markdown_file.read()

    markdown_data_expected = """
---
identifier: ISBN 000-0-0000000-0-0
language: en-US
title: Some Title
author: Some Author
publisher: Some Publisher
copyright: Copyright © 2020 Some Author
version_identifier: 1.0.0
---



# Some Title



## Foreword

Foreword text



## Chapter 1

Chapter 1 paragraph 1

Chapter 1 paragraph 2

Chapter 1 paragraph 3



## Chapter 2

Chapter 2 paragraph 1

Chapter 2 paragraph 2

Chapter 2 paragraph 3



## Chapter 3

Chapter 3 paragraph 1

Chapter 3 paragraph 2

Chapter 3 paragraph 3
"""

    markdown_data_expected = markdown_data_expected.lstrip()

    assert markdown_data == markdown_data_expected


def test_convert_odt_to_markdown_as_many_documents(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToMarkdownConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_directory = os.path.join(workspace_directory, "SectionsAsMarkdown")

    _setup_workspace(workspace_directory)

    convert_odt_to_markdown(
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path_or_directory = output_directory,
        write_as_single_file = False,
        simulate = False,
    )

    _assert_output_as_many_documents(workspace_directory)


def test_convert_odt_to_markdown_as_many_documents_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "OdtToMarkdownConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.fodt")
    output_directory = os.path.join(workspace_directory, "SectionsAsMarkdown")

    _setup_workspace(workspace_directory)

    convert_odt_to_markdown(
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path_or_directory = output_directory,
        write_as_single_file = False,
        simulate = True,
    )

    assert not os.path.exists(output_directory)


def _assert_output_as_many_documents(workspace_directory: str) -> None:
    output_directory = os.path.join(workspace_directory, "SectionsAsMarkdown")

    files_in_destination = os.listdir(output_directory)
    files_in_destination_expected = [
        "0 - Information.yaml",
        "1 - Foreword.md",
        "2 - Chapter 1.md",
        "3 - Chapter 2.md",
        "4 - Chapter 3.md",
    ]

    assert files_in_destination == files_in_destination_expected

    metadata_file_path = os.path.join(output_directory, "0 - Information.yaml")
    with open(metadata_file_path, mode = "r", encoding = "utf-8") as metadata_file:
        metadata_data = metadata_file.read()

    metadata_data_expected = """
identifier: ISBN 000-0-0000000-0-0
language: en-US
title: Some Title
author: Some Author
publisher: Some Publisher
copyright: Copyright © 2020 Some Author
version_identifier: 1.0.0
"""

    metadata_data_expected = metadata_data_expected.lstrip()

    assert metadata_data == metadata_data_expected

    markdown_file_path = os.path.join(output_directory, "1 - Foreword.md")
    with open(markdown_file_path, mode = "r", encoding = "utf-8") as markdown_file:
        markdown_data = markdown_file.read()

    markdown_data_expected = """
# Foreword

Foreword text
"""

    markdown_data_expected = markdown_data_expected.lstrip()

    assert markdown_data == markdown_data_expected

    for chapter_number in [ 1, 2, 3 ]:
        markdown_file_path = os.path.join(output_directory,
            "{index} - Chapter {chapter_number}.md".format(index = chapter_number + 1, chapter_number = chapter_number))
        with open(markdown_file_path, mode = "r", encoding = "utf-8") as markdown_file:
            markdown_data = markdown_file.read()

        markdown_data_expected = """
# Chapter {chapter_number}

Chapter {chapter_number} paragraph 1

Chapter {chapter_number} paragraph 2

Chapter {chapter_number} paragraph 3
"""

        markdown_data_expected = markdown_data_expected.lstrip().format(chapter_number = chapter_number)

        assert markdown_data == markdown_data_expected
