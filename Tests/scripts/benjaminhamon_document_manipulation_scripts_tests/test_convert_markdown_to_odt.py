# cspell:words fodt opendocument

import os

from benjaminhamon_document_manipulation_scripts.convert_markdown_to_odt import convert_markdown_to_odt
from benjaminhamon_document_manipulation_scripts.convert_markdown_to_odt import create_serializer


def test_convert_markdown_to_odt(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "MarkdownToOdtConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.md")
    output_file_path = os.path.join(workspace_directory, "FullText.fodt")

    _setup_workspace(workspace_directory)

    convert_markdown_to_odt(
        serializer = create_serializer("yaml"),
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path = output_file_path,
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_convert_markdown_to_odt_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    configuration_file_path = os.path.join(workspace_directory, "MarkdownToOdtConfiguration.yaml")
    source_file_path = os.path.join(workspace_directory, "FullText.md")
    output_file_path = os.path.join(workspace_directory, "FullText.fodt")

    _setup_workspace(workspace_directory)

    convert_markdown_to_odt(
        serializer = create_serializer("yaml"),
        configuration_file_path = configuration_file_path,
        definition_file_path = None,
        source_file_path = source_file_path,
        destination_file_path = output_file_path,
        simulate = True,
    )

    assert not os.path.exists(output_file_path)


def _setup_workspace(workspace_directory: str) -> None:

    os.makedirs(workspace_directory)

    configuration_file_path = os.path.join(workspace_directory, "MarkdownToOdtConfiguration.yaml")
    with open(configuration_file_path, mode = "w", encoding = "utf-8") as configuration_file:
        configuration_file.write("{}")

    source_file_path = os.path.join(workspace_directory, "FullText.md")

    markdown_data = """
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

    markdown_data = markdown_data.lstrip()

    with open(source_file_path, mode = "w", encoding = "utf-8") as source_file:
        source_file.write(markdown_data)


def _assert_output(workspace_directory: str) -> None:
    output_file_path = os.path.join(workspace_directory, "FullText.fodt")

    assert os.path.exists(output_file_path)

    with open(output_file_path, mode = "r", encoding = "utf-8") as output_file:
        fodt_data = output_file.read()

    fodt_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Some Title</text:span></text:h>
      <text:h><text:span>Foreword</text:span></text:h>
      <text:p><text:span>Foreword text</text:span></text:p>
      <text:h><text:span>Chapter 1</text:span></text:h>
      <text:p><text:span>Chapter 1 paragraph 1</text:span></text:p>
      <text:p><text:span>Chapter 1 paragraph 2</text:span></text:p>
      <text:p><text:span>Chapter 1 paragraph 3</text:span></text:p>
      <text:h><text:span>Chapter 2</text:span></text:h>
      <text:p><text:span>Chapter 2 paragraph 1</text:span></text:p>
      <text:p><text:span>Chapter 2 paragraph 2</text:span></text:p>
      <text:p><text:span>Chapter 2 paragraph 3</text:span></text:p>
      <text:h><text:span>Chapter 3</text:span></text:h>
      <text:p><text:span>Chapter 3 paragraph 1</text:span></text:p>
      <text:p><text:span>Chapter 3 paragraph 2</text:span></text:p>
      <text:p><text:span>Chapter 3 paragraph 3</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    fodt_data_expected = fodt_data_expected.lstrip()

    assert fodt_data == fodt_data_expected
