# cspell:words lxml
# pylint: disable = line-too-long

""" Unit tests for HtmlReader """

import lxml.etree
import lxml.html.html5parser
import pytest

from benjaminhamon_document_manipulation_toolkit.html.html_reader import HtmlReader
from benjaminhamon_document_manipulation_toolkit.html.html_to_document_converter import HtmlToDocumentConverter
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_reader import MarkdownReader
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_to_html_converter import MarkdownToHtmlConverter


def test_read_content():

# cspell:disable
    markdown_data = """
# My document

## Section 1 - The first section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.
"""
# cspell:enable

    markdown_data = markdown_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    document_content = markdown_reader.read_content_from_string(markdown_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    title_section = next(document_content.enumerate_sections())

    assert title_section.get_heading().get_title() == "My document"
    assert sum(1 for _ in title_section.enumerate_paragraphs()) == 0
    assert sum(1 for _ in title_section.enumerate_subsections()) == 1

    content_section = next(title_section.enumerate_subsections())

    assert content_section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in content_section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in content_section.enumerate_subsections()) == 0

    all_paragraphs = list(content_section.enumerate_paragraphs())

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


def test_read_content_with_text_before():

# cspell:disable
    markdown_data = """
Text before title

# My document

## Section 1 - The first section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.
"""
# cspell:enable

    markdown_data = markdown_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    with pytest.raises(ValueError):
        markdown_reader.read_content_from_string(markdown_data)


def test_read_content_with_yaml_header():

# cspell:disable
    markdown_data = """
---
# some comment
SomeField: SomeValue
---

# My document

## Section 1 - The first section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.
"""
# cspell:enable

    markdown_data = markdown_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    document_content = markdown_reader.read_content_from_string(markdown_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    title_section = next(document_content.enumerate_sections())

    assert title_section.get_heading().get_title() == "My document"
    assert sum(1 for _ in title_section.enumerate_paragraphs()) == 0
    assert sum(1 for _ in title_section.enumerate_subsections()) == 1

    content_section = next(title_section.enumerate_subsections())

    assert content_section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in content_section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in content_section.enumerate_subsections()) == 0

    all_paragraphs = list(content_section.enumerate_paragraphs())

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


def test_read_content_with_several_top_level_sections():

# cspell:disable
    markdown_data = """
# Section 1 - The first section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

# Section 2 - The second section

Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.
"""
# cspell:enable

    markdown_data = markdown_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    document_content = markdown_reader.read_content_from_string(markdown_data)
    top_level_sections = list(document_content.enumerate_sections())

    assert len(top_level_sections) == 2

    section = top_level_sections[0]

    assert section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
# cspell:enable
    assert text_elements[0].style_collection == []

    section = top_level_sections[1]

    assert section.get_heading().get_title() == "Section 2 - The second section"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
# cspell:enable
    assert text_elements[0].style_collection == []


def test_read_content_with_styling():

# cspell:disable
    markdown_data = """
# My document

## Section 1 - The first section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. *Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui.* Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. ***Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi.*** Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.
"""
# cspell:enable

    markdown_data = markdown_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    document_content = markdown_reader.read_content_from_string(markdown_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    title_section = next(document_content.enumerate_sections())

    assert title_section.get_heading().get_title() == "My document"
    assert sum(1 for _ in title_section.enumerate_paragraphs()) == 0
    assert sum(1 for _ in title_section.enumerate_subsections()) == 1

    content_section = next(title_section.enumerate_subsections())

    assert content_section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in content_section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in content_section.enumerate_subsections()) == 0

    all_paragraphs = list(content_section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 5
# cspell:disable

# Lorem ipsum dolor sit amet, consectetur adipiscing elit. <span>Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui.</span> Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. <span>Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi.</span> Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    assert text_elements[1].text == "Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui."
    assert text_elements[2].text == " Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. "
    assert text_elements[3].text == "Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi."
    assert text_elements[4].text == " Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
# cspell:enable
    assert text_elements[0].style_collection == []
    assert text_elements[1].style_collection == [ "italic" ]
    assert text_elements[2].style_collection == []
    assert text_elements[3].style_collection == [ "bold", "italic" ]
    assert text_elements[4].style_collection == []

    paragraph = all_paragraphs[1]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
# cspell:enable
    assert text_elements[0].style_collection == []


def test_read_content_with_spans():

# cspell:disable
    markdown_data = """
# My document

## Section 1 - The first section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. <span class="emphasis">Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui.</span> Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. <span class="emphasis">Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi.</span> Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.
"""
# cspell:enable

    markdown_data = markdown_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    document_content = markdown_reader.read_content_from_string(markdown_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    title_section = next(document_content.enumerate_sections())

    assert title_section.get_heading().get_title() == "My document"
    assert sum(1 for _ in title_section.enumerate_paragraphs()) == 0
    assert sum(1 for _ in title_section.enumerate_subsections()) == 1

    content_section = next(title_section.enumerate_subsections())

    assert content_section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in content_section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in content_section.enumerate_subsections()) == 0

    all_paragraphs = list(content_section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 5
# cspell:disable

# Lorem ipsum dolor sit amet, consectetur adipiscing elit. <span>Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui.</span> Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. <span>Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi.</span> Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.

    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    assert text_elements[1].text == "Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui."
    assert text_elements[2].text == " Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. "
    assert text_elements[3].text == "Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi."
    assert text_elements[4].text == " Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
# cspell:enable
    assert text_elements[0].style_collection == []
    assert text_elements[1].style_collection == [ "emphasis" ]
    assert text_elements[2].style_collection == []
    assert text_elements[3].style_collection == [ "emphasis" ]
    assert text_elements[4].style_collection == []

    paragraph = all_paragraphs[1]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
# cspell:enable
    assert text_elements[0].style_collection == []
