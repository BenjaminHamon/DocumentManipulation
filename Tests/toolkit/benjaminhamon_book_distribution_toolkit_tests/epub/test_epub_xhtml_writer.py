""" Unit tests for EpubXhtmlWriter """

import os

from benjaminhamon_book_distribution_toolkit.documents import document_element_factory
from benjaminhamon_book_distribution_toolkit.documents.root_element import RootElement
from benjaminhamon_book_distribution_toolkit.epub.epub_xhtml_writer import EpubXhtmlWriter


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


def test_write_as_many_documents(tmpdir):
    xhtml_writer = EpubXhtmlWriter()

    document = create_document()
    xhtml_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(xhtml_directory)
    xhtml_writer.write_as_many_documents(xhtml_directory, document, simulate = False)

    assert len(os.listdir(xhtml_directory)) == 2

    xhtml_file_path = os.path.join(xhtml_directory, "1 - Section 1.xhtml")

    assert os.path.exists(xhtml_file_path)

    with open(xhtml_file_path, mode = "r", encoding = "utf-8") as xhtml_file:
        actual_content = xhtml_file.read()

    expected_content = """
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Section 1</title>
  </head>
  <body>
    <section>
      <h1>
        <span>Section 1</span>
      </h1>
      <p>
        <span>Some text for the first section.</span>
      </p>
      <p>
        <span>And a second paragraph for the first section.</span>
      </p>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    xhtml_file_path = os.path.join(xhtml_directory, "2 - Section 2.xhtml")

    assert os.path.exists(xhtml_file_path)

    with open(xhtml_file_path, mode = "r", encoding = "utf-8") as xhtml_file:
        actual_content = xhtml_file.read()

    expected_content = """
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Section 2</title>
  </head>
  <body>
    <section>
      <h1>
        <span>Section 2</span>
      </h1>
      <p>
        <span>Some text for the second section.</span>
      </p>
      <p>
        <span>And a second paragraph for the second section.</span>
      </p>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_many_documents_with_simulate(tmpdir):
    xhtml_writer = EpubXhtmlWriter()

    document = create_document()
    xhtml_directory = os.path.join(tmpdir, "Working", "MyDocument")

    xhtml_writer.write_as_many_documents(xhtml_directory, document, simulate = True)

    assert not os.path.exists(xhtml_directory)
