# cspell:words lxml

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers


class DocumentToXhtmlConverter:


    def convert(self,
            xhtml_document: lxml.etree._ElementTree,
            content: RootElement) -> lxml.etree._ElementTree:

        body_as_html = epub_xhtml_helpers.find_xhtml_element(xhtml_document.getroot(), "./x:body")
        for section in content.enumerate_sections():
            body_as_html.append(self._convert_section(section, level = 1))

        return xhtml_document


    def _convert_section(self, section_element: SectionElement, level: int) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(section_element)
        section_as_html = epub_xhtml_helpers.create_xhtml_element("section", attributes = attributes)

        section_as_html.append(self._convert_heading(section_element.get_heading(), level))
        for paragraph_element in section_element.enumerate_paragraphs():
            section_as_html.append(self._convert_paragraph(paragraph_element))
        for subsection_element in section_element.enumerate_subsections():
            section_as_html.append(self._convert_section(subsection_element, level + 1))

        return section_as_html


    def _convert_heading(self, heading_element: HeadingElement, level: int) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(heading_element)
        heading_as_html = epub_xhtml_helpers.create_xhtml_element("h" + str(level), attributes = attributes)

        for text_element in heading_element.enumerate_text():
            heading_as_html.append(self._convert_text(text_element))

        return heading_as_html


    def _convert_paragraph(self, paragraph_element: ParagraphElement) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(paragraph_element)
        paragraph_as_html = epub_xhtml_helpers.create_xhtml_element("p", attributes = attributes)

        for text_element in paragraph_element.enumerate_text():
            paragraph_as_html.append(self._convert_text(text_element))

        if len(paragraph_element.children) == 0:
            paragraph_as_html.text = "\u00a0" # no-break space

        return paragraph_as_html


    def _convert_text(self, text_element: TextElement) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(text_element)
        text_as_html = epub_xhtml_helpers.create_xhtml_element("span", attributes = attributes)
        text_as_html.text = text_element.text
        return text_as_html


    def _get_html_attributes_from_element(self, element: DocumentElement) -> dict:
        attributes = {}

        if element.identifier is not None:
            attributes["id"] = element.identifier
        if len(element.style_collection) > 0:
            attributes["class"] = " ".join(element.style_collection)

        return attributes
