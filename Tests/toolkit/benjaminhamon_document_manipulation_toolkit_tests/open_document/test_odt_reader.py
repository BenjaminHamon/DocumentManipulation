# cspell:words fodt lxml opendocument
# pylint: disable = line-too-long

""" Unit tests for OdtReader """

import datetime
import os

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_region_end_element import TextRegionEndElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_region_start_element import TextRegionStartElement
from benjaminhamon_document_manipulation_toolkit.open_document.odt_reader import OdtReader


def test_read_metadata_from_fodt():
    fodt_file_path = os.path.join(os.path.dirname(__file__), "empty.fodt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_metadata = odt_reader.read_metadata_from_file(fodt_file_path)

    assert document_metadata["title"] == "My Document"
    assert document_metadata["author"] == "Benjamin Hamon"
    assert document_metadata["revision"] == 1
    assert document_metadata["creation_date"] is not None
    assert document_metadata["creation_date"].tzinfo == datetime.timezone.utc
    assert document_metadata["update_date"] is not None
    assert document_metadata["update_date"].tzinfo == datetime.timezone.utc


def test_read_metadata_from_odt():
    odt_file_path = os.path.join(os.path.dirname(__file__), "empty.odt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_metadata = odt_reader.read_metadata_from_file(odt_file_path)

    assert document_metadata["title"] == "My Document"
    assert document_metadata["author"] == "Benjamin Hamon"
    assert document_metadata["revision"] == 1
    assert document_metadata["creation_date"] is not None
    assert document_metadata["creation_date"].tzinfo == datetime.timezone.utc
    assert document_metadata["update_date"] is not None
    assert document_metadata["update_date"].tzinfo == datetime.timezone.utc


def test_read_content_from_empty_fodt():
    fodt_file_path = os.path.join(os.path.dirname(__file__), "empty.fodt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_file(fodt_file_path)

    assert len(document_content.children) == 0


def test_read_content_from_empty_odt():
    odt_file_path = os.path.join(os.path.dirname(__file__), "empty.odt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_file(odt_file_path)

    assert sum(1 for _ in document_content.enumerate_sections()) == 0


def test_read_content_from_simple_fodt():
    fodt_file_path = os.path.join(os.path.dirname(__file__), "simple.fodt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_file(fodt_file_path)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "My heading"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    paragraph = next(section.enumerate_paragraphs())
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 3
    assert text_elements[0].text == "This is a sentence with "
    assert text_elements[0].style_collection == []
    assert text_elements[1].text == "emphasis"
    assert text_elements[1].style_collection == [ "Emphasis" ]
    assert text_elements[2].text == ". And then it ends."
    assert text_elements[2].style_collection == []


def test_read_content_from_simple_odt():
    odt_file_path = os.path.join(os.path.dirname(__file__), "simple.odt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_file(odt_file_path)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "My heading"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    paragraph = next(section.enumerate_paragraphs())
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 3
    assert text_elements[0].text == "This is a sentence with "
    assert text_elements[0].style_collection == []
    assert text_elements[1].text == "emphasis"
    assert text_elements[1].style_collection == [ "Emphasis" ]
    assert text_elements[2].text == ". And then it ends."
    assert text_elements[2].style_collection == []


def test_read_content_from_clean_fodt():

# cspell:disable
    fodt_data = """
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h>
        <text:span>Chapter 1</text:span><text:line-break/><text:span>The first chapter</text:span>
      </text:h>
      <text:p>
        <text:span>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.</text:span>
      </text:p>
      <text:p>
        <text:span>Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.</text:span>
      </text:p>
    </office:text>
  </office:body>
</office:document>
"""
# cspell:enable

    fodt_data = fodt_data.lstrip()

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_string(fodt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "Chapter 1 - The first chapter"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
# cspell:enable
    assert text_elements[0].style_collection == []

    paragraph = all_paragraphs[1]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
# cspell:enable
    assert text_elements[0].style_collection == []


def test_read_content_with_soft_page_breaks():
    fodt_data = """
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h>The Section</text:h>
      <text:p>Some text with a soft page break <text:soft-page-break/>somewhere.</text:p>
      <text:p>Some text with a soft page break inside-<text:soft-page-break/>dashes.</text:p>
      <text:p><text:soft-page-break/>Some text with a soft page break at the start.</text:p>
      <text:p><text:span text:style-name="span-style"><text:soft-page-break/>Some text with a soft page break at the start and a span with a style.</text:span></text:p>
    </office:text>
  </office:body>
</office:document>
    """

    fodt_data = fodt_data.lstrip()

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_string(fodt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "The Section"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 4
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Some text with a soft page break somewhere."
    assert text_elements[0].style_collection == []

    paragraph = all_paragraphs[1]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Some text with a soft page break inside-dashes."
    assert text_elements[0].style_collection == []

    paragraph = all_paragraphs[2]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Some text with a soft page break at the start."
    assert text_elements[0].style_collection == []

    paragraph = all_paragraphs[3]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Some text with a soft page break at the start and a span with a style."
    assert text_elements[0].style_collection == [ "span-style" ]


def test_read_content_with_comments():
    fodt_data = """
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h>The Section</text:h>
      <text:p>Before the comment. <office:annotation office:name="__Annotation__123"><dc:creator>Benjamin Hamon</dc:creator><dc:date>2020-01-01T00:00:00</dc:date><text:p>Some comment</text:p></office:annotation>Inside the comment.</text:p>
      <text:p>Inside the comment again.<office:annotation-end office:name="__Annotation__123"/> After the comment.</text:p>
    </office:text>
  </office:body>
</office:document>
    """

    fodt_data = fodt_data.lstrip()

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content_from_string(fodt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "The Section"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]

    assert len(paragraph.children) == 3
    assert isinstance(paragraph.children[0], TextElement)
    assert paragraph.children[0].text == "Before the comment. "
    assert paragraph.children[0].style_collection == []
    assert isinstance(paragraph.children[1], TextRegionStartElement)
    assert paragraph.children[1].identifier == "__Annotation__123"
    assert isinstance(paragraph.children[2], TextElement)
    assert paragraph.children[2].text == "Inside the comment."
    assert paragraph.children[2].style_collection == []

    paragraph = all_paragraphs[1]

    assert len(paragraph.children) == 3
    assert isinstance(paragraph.children[0], TextElement)
    assert paragraph.children[0].text == "Inside the comment again."
    assert paragraph.children[0].style_collection == []
    assert isinstance(paragraph.children[1], TextRegionEndElement)
    assert paragraph.children[1].identifier == "__Annotation__123"
    assert isinstance(paragraph.children[2], TextElement)
    assert paragraph.children[2].text == " After the comment."
    assert paragraph.children[2].style_collection == []


def test_read_comments():
    fodt_data = """
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h>The Section</text:h>
      <text:p>Before the comment. <office:annotation office:name="__Annotation__123"><dc:creator>Benjamin Hamon</dc:creator><dc:date>2020-01-01T00:00:00</dc:date><text:p><text:span>Some comment.</text:span></text:p><text:p><text:span>More text in the comment.</text:span></text:p></office:annotation>Inside the comment.</text:p>
      <text:p>Inside the comment again.<office:annotation-end office:name="__Annotation__123"/> After the comment.</text:p>
    </office:text>
  </office:body>
</office:document>
    """

    fodt_data = fodt_data.lstrip()

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_comments = odt_reader.read_comments_from_string(fodt_data)

    assert len(document_comments) == 1
    assert document_comments[0].region_identifier == "__Annotation__123"
    assert document_comments[0].author == "Benjamin Hamon"
    assert document_comments[0].date == datetime.datetime(2020, 1, 1)
    assert document_comments[0].text == "Some comment.\nMore text in the comment."
