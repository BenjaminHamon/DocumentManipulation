# cspell:words lxml nsmap

from typing import List, Optional

import lxml.etree

from benjaminhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_book_distribution_toolkit.documents.root_element import RootElement
from benjaminhamon_book_distribution_toolkit.documents.section_element import SectionElement
from benjaminhamon_book_distribution_toolkit.documents.text_element import TextElement
from benjaminhamon_book_distribution_toolkit.open_document import odt_operations


class OdtBuilder:


    def __init__(self, xml_document_base: lxml.etree._ElementTree) -> None:
        self._xml_document = xml_document_base


    def get_xml_document(self) -> lxml.etree._ElementTree:
        return self._xml_document


    def add_content(self, root_element: RootElement) -> None:
        for section_element in root_element.enumerate_sections():
            self.add_section(section_element)


    def add_section(self, section_element: SectionElement) -> None:
        self.add_heading(section_element.get_heading())

        for paragraph in section_element.enumerate_paragraphs():
            self.add_paragraph(paragraph)

        for subsection in section_element.enumerate_subsections():
            self.add_section(subsection)


    def add_heading(self, heading_element: HeadingElement) -> None:
        heading_as_xml = self._create_text_xml_element(None, "h", heading_element.style_collection, None)

        for text_element in heading_element.enumerate_text():
            self.add_text(heading_as_xml, text_element)


    def add_paragraph(self, paragraph_element: ParagraphElement) -> None:
        paragraph_as_xml = self._create_text_xml_element(None, "p", paragraph_element.style_collection, None)

        for text_element in paragraph_element.enumerate_text():
            self.add_text(paragraph_as_xml, text_element)


    def add_text(self, paragraph_as_xml: lxml.etree._Element, text_element: TextElement) -> None:
        self._create_text_xml_element(paragraph_as_xml, "span", text_element.style_collection, text_element.text)
        if text_element.line_break:
            self._create_line_break_element(paragraph_as_xml)


    def _create_text_xml_element(self,
            parent: Optional[lxml.etree._Element], tag: str, style_collection: List[str], text: Optional[str]) -> lxml.etree._Element:

        body_as_xml = odt_operations.get_body_text_element(self._xml_document)
        if parent is None:
            parent = body_as_xml

        attributes = {}
        if len(style_collection) > 1:
            raise ValueError("Too many styles")
        if len(style_collection) == 1:
            attributes[lxml.etree.QName(body_as_xml.nsmap["text"], "style-name")] = style_collection[0]

        element = lxml.etree.SubElement(parent, lxml.etree.QName(body_as_xml.nsmap["text"], tag), attrib = attributes)
        element.text = text

        return element


    def _create_line_break_element(self, parent: Optional[lxml.etree._Element]) -> lxml.etree._Element:
        body_as_xml = odt_operations.get_body_text_element(self._xml_document)
        if parent is None:
            parent = body_as_xml

        tag = lxml.etree.QName(body_as_xml.nsmap["text"], "line-break")
        element = lxml.etree.SubElement(parent, tag)

        return element
