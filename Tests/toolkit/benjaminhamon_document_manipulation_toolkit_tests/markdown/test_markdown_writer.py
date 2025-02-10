""" Unit tests for MarkdownWriter """

import os

from benjaminhamon_document_manipulation_toolkit.documents import document_element_factory
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.markdown.document_to_markdown_converter import DocumentToMarkdownConverter
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_writer import MarkdownWriter
from benjaminhamon_document_manipulation_toolkit.serialization.yaml_serializer import YamlSerializer


def create_document() -> RootElement:
    document = RootElement()

    document.children.append(
        document_element_factory.create_section(
            heading = "Section 1",
            text = [
                [ "Some text for the first section." ],
                [ "And a second paragraph for the first section." ]
            ],
        )
    )

    document.children.append(
        document_element_factory.create_section(
            heading = "Section 2",
            text = [
                [ "Some text for the second section." ],
                [ "And a second paragraph for the second section." ]
            ],
        )
    )

    return document


def test_write_as_single_document(tmpdir):
    markdown_writer = MarkdownWriter(DocumentToMarkdownConverter(), YamlSerializer())

    metadata = { "author": "The Author" }
    document = create_document()
    markdown_file_path = os.path.join(tmpdir, "Working", "MyDocument.md")

    os.makedirs(os.path.dirname(markdown_file_path))
    markdown_writer.write_as_single_document(markdown_file_path, "The Title", metadata, document, simulate = False)

    assert os.path.exists(markdown_file_path)

    with open(markdown_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
---
author: The Author
---



# The Title



## Section 1

Some text for the first section.

And a second paragraph for the first section.



## Section 2

Some text for the second section.

And a second paragraph for the second section.
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_single_document_with_simulate(tmpdir):
    markdown_writer = MarkdownWriter(DocumentToMarkdownConverter(), YamlSerializer())

    metadata = { "author": "The Author" }
    document = create_document()
    markdown_file_path = os.path.join(tmpdir, "Working", "MyDocument.md")

    os.makedirs(os.path.dirname(markdown_file_path))
    markdown_writer.write_as_single_document(markdown_file_path, "The Title", metadata, document, simulate = True)

    assert not os.path.exists(markdown_file_path)


def test_write_as_many_documents(tmpdir):
    markdown_writer = MarkdownWriter(DocumentToMarkdownConverter(), YamlSerializer())

    metadata = { "author": "The Author" }
    document = create_document()
    markdown_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(markdown_directory)
    markdown_writer.write_as_many_documents(markdown_directory, metadata, document, simulate = False)

    assert len(os.listdir(markdown_directory)) == 3

    markdown_file_path = os.path.join(markdown_directory, "0 - Information.yaml")

    assert os.path.exists(markdown_file_path)

    with open(markdown_file_path, mode = "r", encoding = "utf-8") as markdown_file:
        actual_content = markdown_file.read()

    expected_content = """
author: The Author
"""

    markdown_file_path = os.path.join(markdown_directory, "1 - Section 1.md")

    assert os.path.exists(markdown_file_path)

    with open(markdown_file_path, mode = "r", encoding = "utf-8") as markdown_file:
        actual_content = markdown_file.read()

    expected_content = """
# Section 1

Some text for the first section.

And a second paragraph for the first section.
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    markdown_file_path = os.path.join(markdown_directory, "2 - Section 2.md")

    assert os.path.exists(markdown_file_path)

    with open(markdown_file_path, mode = "r", encoding = "utf-8") as markdown_file:
        actual_content = markdown_file.read()

    expected_content = """
# Section 2

Some text for the second section.

And a second paragraph for the second section.
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_many_documents_with_simulate(tmpdir):
    markdown_writer = MarkdownWriter(DocumentToMarkdownConverter(), YamlSerializer())

    metadata = { "author": "The Author" }
    document = create_document()
    markdown_directory = os.path.join(tmpdir, "Working", "MyDocument")

    markdown_writer.write_as_many_documents(markdown_directory, metadata, document, simulate = True)

    assert not os.path.exists(markdown_directory)
