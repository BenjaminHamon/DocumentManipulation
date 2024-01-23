# cspell:words fodt lxml opendocument
# pylint: disable = line-too-long

""" Unit tests for OdtReader """

import datetime
import os

import lxml.etree

from benjaminhamon_book_distribution_toolkit.open_document.odt_reader import OdtReader


def test_read_metadata_from_fodt():
    fodt_file_path = os.path.join(os.path.dirname(__file__), "empty.fodt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    fodt_data = odt_reader.read_fodt(fodt_file_path)
    document_metadata = odt_reader.read_metadata(fodt_data)

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

    odt_data = odt_reader.read_odt(odt_file_path, "meta.xml")
    document_metadata = odt_reader.read_metadata(odt_data)

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

    fodt_data = odt_reader.read_fodt(fodt_file_path)
    document_content = odt_reader.read_content(fodt_data)

    assert len(document_content.children) == 0


def test_read_content_from_empty_odt():
    odt_file_path = os.path.join(os.path.dirname(__file__), "empty.odt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    odt_data = odt_reader.read_odt(odt_file_path, "content.xml")
    document_content = odt_reader.read_content(odt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 0


def test_read_content_from_simple_fodt():
    fodt_file_path = os.path.join(os.path.dirname(__file__), "simple.fodt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    fodt_data = odt_reader.read_fodt(fodt_file_path)
    document_content = odt_reader.read_content(fodt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "My heading"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    paragraph = next(section.enumerate_paragraphs())
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 3
    assert text_elements[0].text == "This is a sentence with"
    assert text_elements[0].style_collection == []
    assert text_elements[1].text == "emphasis"
    assert text_elements[1].style_collection == [ "Emphasis" ]
    assert text_elements[2].text == ". And then it ends."
    assert text_elements[2].style_collection == []


def test_read_content_from_simple_odt():
    odt_file_path = os.path.join(os.path.dirname(__file__), "simple.odt")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    odt_data = odt_reader.read_odt(odt_file_path, "content.xml")
    document_content = odt_reader.read_content(odt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "My heading"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    paragraph = next(section.enumerate_paragraphs())
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 3
    assert text_elements[0].text == "This is a sentence with"
    assert text_elements[0].style_collection == []
    assert text_elements[1].text == "emphasis"
    assert text_elements[1].style_collection == [ "Emphasis" ]
    assert text_elements[2].text == ". And then it ends."
    assert text_elements[2].style_collection == []


def test_read_content_from_clean_fodt():
    fodt_data = """
<?xml version="1.0" encoding="utf-8"?>
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

    fodt_data = fodt_data.lstrip().encode("utf-8")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content(fodt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "Chapter 1 - The first chapter"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
    assert text_elements[0].style_collection == []

    paragraph = all_paragraphs[1]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
    assert text_elements[0].style_collection == []


def test_read_content_from_original_fodt():
    fodt_data = """
<?xml version="1.0" encoding="utf-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <text:h>Chapter 1<text:line-break/>The first chapter</text:h>
      <text:p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.</text:p>
      <text:p><text:soft-page-break/>Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. <text:soft-page-break/>Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.</text:p>
    </office:text>
  </office:body>
</office:document>
    """

    fodt_data = fodt_data.lstrip().encode("utf-8")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)

    document_content = odt_reader.read_content(fodt_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "Chapter 1 - The first chapter"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
    assert text_elements[0].style_collection == []

    paragraph = all_paragraphs[1]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
    assert text_elements[0].style_collection == []
