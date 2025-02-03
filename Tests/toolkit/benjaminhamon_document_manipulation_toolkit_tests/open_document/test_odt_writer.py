# cspell:words fodt lxml opendocument

""" Unit tests for OdtWriter """

import datetime
import os
import zipfile

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents import document_element_factory
from benjaminhamon_document_manipulation_toolkit.documents.elements.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_region_end_element import TextRegionEndElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_region_start_element import TextRegionStartElement
from benjaminhamon_document_manipulation_toolkit.open_document.odt_writer import OdtWriter


def create_generic_document() -> RootElement:
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

    document = create_generic_document()
    fodt_file_path = os.path.join(tmpdir, "Working", "MyDocument.fodt")

    os.makedirs(os.path.dirname(fodt_file_path))
    odt_writer.write_as_single_document(fodt_file_path, document, [], flat_odt = True, simulate = False)

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


def test_write_as_single_document_to_fodt_with_comments(tmpdir):

    def create_document() -> RootElement:
        document = RootElement()

        document.children.append(
            document_element_factory.create_section(
                heading = "The Section",
                text = [
                    [ "Before the comment.", "Inside the comment." ],
                    [ "Inside the comment again.", "After the comment." ]
                ],
            )
        )

        return document

    def insert_comment(document: RootElement) -> DocumentComment:
        document.children[0].children[1].children.insert(1, TextRegionStartElement("__Annotation__123"))
        document.children[0].children[2].children.insert(1, TextRegionEndElement("__Annotation__123"))

        return DocumentComment("__Annotation__123", "Benjamin Hamon", datetime.datetime(2020, 1, 1), "Some comment.\nMore text in the comment.")

    def get_expected_fodt() -> str:
        expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>The Section</text:span></text:h>
      <text:p><text:span>Before the comment.</text:span><office:annotation office:name="__Annotation__123"><dc:creator>Benjamin Hamon</dc:creator><dc:date>2020-01-01T00:00:00</dc:date><text:p>Some comment.</text:p><text:p>More text in the comment.</text:p></office:annotation><text:span>Inside the comment.</text:span></text:p>
      <text:p><text:span>Inside the comment again.</text:span><office:annotation-end office:name="__Annotation__123"/><text:span>After the comment.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

        return expected_content.lstrip()

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_document()
    comment = insert_comment(document)
    fodt_file_path = os.path.join(tmpdir, "Working", "MyDocument.fodt")

    os.makedirs(os.path.dirname(fodt_file_path))
    odt_writer.write_as_single_document(fodt_file_path, document, [ comment ], flat_odt = True, simulate = False)

    assert os.path.exists(fodt_file_path)

    expected_content = get_expected_fodt()
    with open(fodt_file_path, mode = "r", encoding = "utf-8") as odt_file:
        actual_content = odt_file.read()

    assert actual_content == expected_content


def test_write_as_single_document_to_fodt_with_template(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_generic_document()
    template_file_path = os.path.join(tmpdir, "Working", "Template.fodt")
    fodt_file_path = os.path.join(tmpdir, "Working", "MyDocument.fodt")

    template_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:meta>
    <meta:user-defined meta:name="Language">English</meta:user-defined>
  </office:meta>
  <office:body>
    <office:text/>
  </office:body>
</office:document>
"""

    template_content = template_content.lstrip()

    os.makedirs(os.path.dirname(fodt_file_path))
    with open(template_file_path, mode = "w", encoding = "utf-8") as template_file:
        template_file.write(template_content)
    odt_writer.write_as_single_document(fodt_file_path, document, [], template_file_path, flat_odt = True, simulate = False)

    assert os.path.exists(fodt_file_path)

    with open(fodt_file_path, mode = "r", encoding = "utf-8") as odt_file:
        actual_content = odt_file.read()

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:meta>
    <meta:user-defined meta:name="Language">English</meta:user-defined>
  </office:meta>
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


def test_write_as_single_document_to_fodt_with_template_and_whitespace(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_generic_document()
    template_file_path = os.path.join(tmpdir, "Working", "Template.fodt")
    fodt_file_path = os.path.join(tmpdir, "Working", "MyDocument.fodt")

    template_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:meta>
    <meta:user-defined meta:name="Language">English</meta:user-defined>
  </office:meta>
  <office:body>
    <office:text>
    </office:text>
  </office:body>
</office:document>
"""

    template_content = template_content.lstrip()

    os.makedirs(os.path.dirname(fodt_file_path))
    with open(template_file_path, mode = "w", encoding = "utf-8") as template_file:
        template_file.write(template_content)
    odt_writer.write_as_single_document(fodt_file_path, document, [], template_file_path, flat_odt = True, simulate = False)

    assert os.path.exists(fodt_file_path)

    with open(fodt_file_path, mode = "r", encoding = "utf-8") as odt_file:
        actual_content = odt_file.read()

    expected_content = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:meta>
    <meta:user-defined meta:name="Language">English</meta:user-defined>
  </office:meta>
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

    document = create_generic_document()
    odt_file_path = os.path.join(tmpdir, "Working", "MyDocument.odt")

    os.makedirs(os.path.dirname(odt_file_path))
    odt_writer.write_as_single_document(odt_file_path, document, [], flat_odt = False, simulate = False)

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

    document = create_generic_document()
    odt_writer.write_as_single_document(fodt_file_path, document, [], flat_odt = True, simulate = True)

    assert not os.path.exists(fodt_file_path)


def test_write_as_single_document_to_odt_with_simulate(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    odt_file_path = os.path.join(tmpdir, "Working", "MyDocument.odt")

    document = create_generic_document()
    odt_writer.write_as_single_document(odt_file_path, document, [], flat_odt = False, simulate = True)

    assert not os.path.exists(odt_file_path)


def test_write_as_many_documents_to_fodt(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_generic_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(odt_directory)
    odt_writer.write_as_many_documents(odt_directory, document, [], flat_odt = True, simulate = False)

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

    document = create_generic_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(odt_directory)
    odt_writer.write_as_many_documents(odt_directory, document, [], flat_odt = False, simulate = False)

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

    document = create_generic_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    odt_writer.write_as_many_documents(odt_directory, document, [], flat_odt = True, simulate = True)

    assert not os.path.exists(odt_directory)


def test_write_as_many_documents_to_odt_with_simulate(tmpdir):
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document = create_generic_document()
    odt_directory = os.path.join(tmpdir, "Working", "MyDocument")

    odt_writer.write_as_many_documents(odt_directory, document, [], flat_odt = False, simulate = True)

    assert not os.path.exists(odt_directory)


def test_collapse_body_elements():
    document = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h>
        <text:span>The Section</text:span>
      </text:h>
      <text:p>
        <text:span>This paragraph has </text:span>
        <text:span text:style-name="a_style">styled text</text:span>
        <text:span> in the middle.</text:span>
      </text:p>
      <text:p>
        <text:span>This paragraph has </text:span>
        <office:annotation office:name="__Annotation__123">
          <dc:creator>Benjamin Hamon</dc:creator>
          <dc:date>2020-01-01T00:00:00</dc:date>
          <text:p>Here is the comment.</text:p>
          <text:p>And a second paragraph in the comment.</text:p>
        </office:annotation>
        <text:span>some of its text commented</text:span>
        <office:annotation-end office:name="__Annotation__123"/>
        <text:span> and then more text.</text:span>
      </text:p>
    </office:text>
  </office:body>
</office:document>
"""

    document = document.lstrip()

    document_formatted_expected = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h><text:span>The Section</text:span></text:h>
      <text:p><text:span>This paragraph has </text:span><text:span text:style-name="a_style">styled text</text:span><text:span> in the middle.</text:span></text:p>
      <text:p><text:span>This paragraph has </text:span><office:annotation office:name="__Annotation__123"><dc:creator>Benjamin Hamon</dc:creator><dc:date>2020-01-01T00:00:00</dc:date><text:p>Here is the comment.</text:p><text:p>And a second paragraph in the comment.</text:p></office:annotation><text:span>some of its text commented</text:span><office:annotation-end office:name="__Annotation__123"/><text:span> and then more text.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
"""

    document_formatted_expected = document_formatted_expected.lstrip()

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(xml_parser)

    document_formatted_actual = odt_writer._collapse_body_elements(document) # pylint: disable = protected-access

    assert document_formatted_actual == document_formatted_expected
