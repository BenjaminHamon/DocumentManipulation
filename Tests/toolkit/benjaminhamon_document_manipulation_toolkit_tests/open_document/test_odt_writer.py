# cspell:words fodt lxml opendocument

""" Unit tests for OdtWriter """

import os
import zipfile

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents import document_element_factory
from benjaminhamon_document_manipulation_toolkit.documents.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.open_document.odt_writer import OdtWriter


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


def test_write_as_single_document_to_fodt(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    fodt_file_path = os.path.join(tmpdir, "Working", "MyDocument.fodt")

    os.makedirs(os.path.dirname(fodt_file_path))
    odt_writer.write_as_single_document(fodt_file_path, document, flat_odt = True, simulate = False)

    assert os.path.exists(fodt_file_path)

    with open(fodt_file_path, mode = "r", encoding = "utf-8") as odt_file:
        actual_content = odt_file.read()

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Section 1</text:span></text:h>
      <text:p><text:span>Some text for the first section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the first section.</text:span></text:p>
      <text:h><text:span>Section 2</text:span></text:h>
      <text:p><text:span>Some text for the second section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the second section.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_single_document_to_odt(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    odt_file_path = os.path.join(tmpdir, "Working", "MyDocument.odt")

    os.makedirs(os.path.dirname(odt_file_path))
    odt_writer.write_as_single_document(odt_file_path, document, flat_odt = False, simulate = False)

    assert os.path.exists(odt_file_path)

    with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
        actual_content = odt_file.read("content.xml").decode("utf-8")

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Section 1</text:span></text:h>
      <text:p><text:span>Some text for the first section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the first section.</text:span></text:p>
      <text:h><text:span>Section 2</text:span></text:h>
      <text:p><text:span>Some text for the second section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the second section.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_single_document_to_fodt_with_simulate(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    fodt_file_path = os.path.join(tmpdir, "Working", "MyDocument.fodt")

    document = create_document()
    odt_writer.write_as_single_document(fodt_file_path, document, flat_odt = True, simulate = True)

    assert not os.path.exists(fodt_file_path)


def test_write_as_single_document_to_odt_with_simulate(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    odt_file_path = os.path.join(tmpdir, "Working", "MyDocument.odt")

    document = create_document()
    odt_writer.write_as_single_document(odt_file_path, document, flat_odt = False, simulate = True)

    assert not os.path.exists(odt_file_path)


def test_write_as_many_documents_to_fodt(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(odt_directory)
    odt_writer.write_as_many_documents(odt_directory, document, flat_odt = True, simulate = False)

    assert len(os.listdir(odt_directory)) == 2

    fodt_file_path = os.path.join(odt_directory, "1 - Section 1.fodt")

    assert os.path.exists(fodt_file_path)

    with open(fodt_file_path, mode = "r", encoding = "utf-8") as fodt_file:
        actual_content = fodt_file.read()

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Section 1</text:span></text:h>
      <text:p><text:span>Some text for the first section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the first section.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    fodt_file_path = os.path.join(odt_directory, "2 - Section 2.fodt")

    assert os.path.exists(fodt_file_path)

    with open(fodt_file_path, mode = "r", encoding = "utf-8") as fodt_file:
        actual_content = fodt_file.read()

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Section 2</text:span></text:h>
      <text:p><text:span>Some text for the second section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the second section.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_many_documents_to_odt(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(odt_directory)
    odt_writer.write_as_many_documents(odt_directory, document, flat_odt = False, simulate = False)

    assert len(os.listdir(odt_directory)) == 2

    odt_file_path = os.path.join(odt_directory, "1 - Section 1.odt")

    assert os.path.exists(odt_file_path)

    with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
        actual_content = odt_file.read("content.xml").decode("utf-8")

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Section 1</text:span></text:h>
      <text:p><text:span>Some text for the first section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the first section.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    odt_file_path = os.path.join(odt_directory, "2 - Section 2.odt")

    assert os.path.exists(odt_file_path)

    with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
        actual_content = odt_file.read("content.xml").decode("utf-8")

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>Section 2</text:span></text:h>
      <text:p><text:span>Some text for the second section.</text:span></text:p>
      <text:p><text:span>And a second paragraph for the second section.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_many_documents_to_fodt_with_simulate(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    odt_writer.write_as_many_documents(odt_directory, document, flat_odt = True, simulate = True)

    assert not os.path.exists(odt_directory)


def test_write_as_many_documents_to_odt_with_simulate(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    odt_writer.write_as_many_documents(odt_directory, document, flat_odt = False, simulate = True)

    assert not os.path.exists(odt_directory)
