# cspell:words lxml

from typing import Mapping
import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.xml import xpath_helpers


class DocumentToHtmlConverter:


    def convert(self, html_document: lxml.etree._ElementTree, title: str, metadata: Mapping[str,str], content: RootElement) -> lxml.etree._ElementTree:
        head_as_html = xpath_helpers.find_xml_element(html_document.getroot(), "./head")
        body_as_html = xpath_helpers.find_xml_element(html_document.getroot(), "./body")

        for key, value in metadata.items():
            meta_as_html = lxml.etree.Element("meta", attrib = { "name": key, "content": value })
            head_as_html.append(meta_as_html)

        root_section_as_html = lxml.etree.Element("section", attrib = self._get_html_attributes_from_element(content))
        heading_as_html = lxml.etree.Element("h1")
        heading_text_as_html = lxml.etree.Element("p")
        heading_text_as_html.text = title
        heading_as_html.append(heading_text_as_html)
        root_section_as_html.append(heading_as_html)
        body_as_html.append(root_section_as_html)

        for section in content.enumerate_sections():
            root_section_as_html.append(self._convert_section(section, level = 2))

        return html_document


    def convert_as_section(self, html_document: lxml.etree._ElementTree, section: SectionElement) -> lxml.etree._ElementTree:
        body_as_html = xpath_helpers.find_xml_element(html_document.getroot(), "./body")
        body_as_html.append(self._convert_section(section, level = 1))

        return html_document


    def _convert_section(self, section_element: SectionElement, level: int) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(section_element)
        section_as_html = lxml.etree.Element("section", attrib = attributes)

        section_as_html.append(self._convert_heading(section_element.get_heading(), level))
        for paragraph_element in section_element.enumerate_paragraphs():
            section_as_html.append(self._convert_paragraph(paragraph_element))
        for subsection_element in section_element.enumerate_subsections():
            section_as_html.append(self._convert_section(subsection_element, level + 1))

        return section_as_html


    def _convert_heading(self, heading_element: HeadingElement, level: int) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(heading_element)
        heading_as_html = lxml.etree.Element("h" + str(level), attrib = attributes)

        for text_element in heading_element.enumerate_text():
            heading_as_html.append(self._convert_text(text_element))

        return heading_as_html


    def _convert_paragraph(self, paragraph_element: ParagraphElement) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(paragraph_element)
        paragraph_as_html = lxml.etree.Element("p", attrib = attributes)

        for text_element in paragraph_element.enumerate_text():
            paragraph_as_html.append(self._convert_text(text_element))

        if len(paragraph_element.children) == 0:
            paragraph_as_html.text = "\u00a0" # no-break space

        return paragraph_as_html


    def _convert_text(self, text_element: TextElement) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(text_element)
        text_as_html = lxml.etree.Element("span", attrib = attributes)
        text_as_html.text = text_element.text
        return text_as_html


    def _get_html_attributes_from_element(self, element: DocumentElement) -> dict:
        attributes = {}

        if element.identifier is not None:
            attributes["id"] = element.identifier
        if len(element.style_collection) > 0:
            attributes["class"] = " ".join(element.style_collection)

        return attributes
