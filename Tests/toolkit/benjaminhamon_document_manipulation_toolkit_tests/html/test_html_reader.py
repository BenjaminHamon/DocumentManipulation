# pylint: disable = line-too-long

""" Unit tests for HtmlReader """

import lxml.etree
import lxml.html.html5parser

from benjaminhamon_document_manipulation_toolkit.html.html_reader import HtmlReader
from benjaminhamon_document_manipulation_toolkit.html.html_to_document_converter import HtmlToDocumentConverter


def test_read_content():

# cspell:disable
    html_data = """
<!doctype html>
<html>
    <head>
        <title>My document</title>
        <link rel="stylesheet" href="static/styles.css"/>
    </head>
    <body>
        <section>
            <h1>Section 1 - The first section</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.</p>
            <p>Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.</p>
        </section>
    </body>
</html>
"""
# cspell:enable

    html_data = html_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)

    document_content = html_reader.read_content_from_string(html_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "Section 1 - The first section"
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


def test_read_content_with_spans():

# cspell:disable
    html_data = """
<!doctype html>
<html>
    <head>
        <title>My document</title>
        <link rel="stylesheet" href="static/styles.css"/>
    </head>
    <body>
        <section>
            <h1>Section 1 - The first section</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. <span class="emphasis">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat.</span> Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. <span class="emphasis">Donec rutrum magna ut tempus accumsan.</span> Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.</p>
            <p>Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.</p>
        </section>
    </body>
</html>
"""
# cspell:enable

    html_data = html_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)

    document_content = html_reader.read_content_from_string(html_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 2
    assert sum(1 for _ in section.enumerate_subsections()) == 0

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 5
# cspell:disable
    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. "
    assert text_elements[1].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat."
    assert text_elements[2].text == " Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. "
    assert text_elements[3].text == "Donec rutrum magna ut tempus accumsan."
    assert text_elements[4].text == " Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
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


def test_read_content_with_subsection():

# cspell:disable
    html_data = """
<!doctype html>
<html>
    <head>
        <title>My document</title>
        <link rel="stylesheet" href="static/styles.css"/>
    </head>
    <body>
        <section>
            <h1>Section 1 - The first section</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim.</p>
            <section>
                <h2>Section 1 - Subsection 1 - A subsection</h2>
                <p>Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla.</p>
            </section>
        </section>
    </body>
</html>
"""
# cspell:enable

    html_data = html_data.lstrip()

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)

    document_content = html_reader.read_content_from_string(html_data)

    assert sum(1 for _ in document_content.enumerate_sections()) == 1

    section = next(document_content.enumerate_sections())

    assert section.get_heading().get_title() == "Section 1 - The first section"
    assert sum(1 for _ in section.enumerate_paragraphs()) == 1
    assert sum(1 for _ in section.enumerate_subsections()) == 1

    all_paragraphs = list(section.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam bibendum lectus ut nisi faucibus dapibus. Integer tincidunt ante dui. Phasellus ullamcorper metus diam, a lobortis lacus sollicitudin ut. In euismod malesuada orci nec viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi vehicula ac arcu imperdiet auctor. Nullam lobortis nec urna vitae feugiat. Nulla metus sem, vehicula in lorem sit amet, interdum ultrices leo. Vivamus at posuere ligula. In fringilla laoreet tellus maximus feugiat. Donec rutrum magna ut tempus accumsan. Vivamus condimentum lacus id magna elementum, a malesuada mauris volutpat. In et purus vel justo ultricies ornare id vitae mi. Etiam bibendum eros ut ligula facilisis, eu vulputate dui aliquam. Phasellus nulla sem, blandit vitae est non, posuere luctus enim."
# cspell:enable
    assert text_elements[0].style_collection == []

    subsection = next(section.enumerate_subsections())
    assert sum(1 for _ in subsection.enumerate_paragraphs()) == 1

    all_paragraphs = list(subsection.enumerate_paragraphs())

    paragraph = all_paragraphs[0]
    text_elements = list(paragraph.enumerate_text())

    assert len(text_elements) == 1
# cspell:disable
    assert text_elements[0].text == "Cras eget neque semper, cursus eros at, bibendum nisl. Morbi accumsan nunc pellentesque, pharetra ipsum vel, convallis libero. Morbi condimentum hendrerit congue. Ut facilisis dolor et lorem facilisis, sagittis lacinia nibh tempor. Nam imperdiet fermentum sem sit amet porttitor. In consectetur vehicula imperdiet. Aliquam eleifend turpis vitae tincidunt fringilla."
# cspell:enable
    assert text_elements[0].style_collection == []
