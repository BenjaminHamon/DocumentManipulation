# cspell:words getroottree fodt lxml nsmap opendocument

from typing import List, Optional
import zipfile

import lxml.etree

from benjaminhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_book_distribution_toolkit.documents.root_element import RootElement
from benjaminhamon_book_distribution_toolkit.documents.section_element import SectionElement
from benjaminhamon_book_distribution_toolkit.documents.text_element import TextElement


class OdtBuilder:


    def __init__(self, template_file_path: Optional[str] = None) -> None:
        self._xml_document = OdtBuilder._create_document(template_file_path)
        self.heading_prefix_style: Optional[str] = None


    @staticmethod
    def _create_document(template_file_path: Optional[str] = None) -> lxml.etree._ElementTree:
        if template_file_path is None:
            namespaces = {
                "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
                "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
            }

            document_element = lxml.etree.Element(lxml.etree.QName(namespaces["office"], "document"), nsmap = namespaces)
            body_element = lxml.etree.SubElement(document_element, lxml.etree.QName(namespaces["office"], "body"))
            lxml.etree.SubElement(body_element, lxml.etree.QName(namespaces["office"], "text"))
            return lxml.etree.ElementTree(document_element)

        xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)

        if template_file_path.endswith(".fodt"):
            return lxml.etree.parse(template_file_path, xml_parser)

        if template_file_path.endswith(".odt"):
            with zipfile.ZipFile(template_file_path, mode = "r") as odt_file:
                odt_content = odt_file.read("content.xml")
            return lxml.etree.fromstring(odt_content).getroottree()

        raise ValueError("Unsupported template file: '%s'" % template_file_path)


    def get_xml_document(self) -> lxml.etree._ElementTree:
        return self._xml_document


    def _get_body_text_element(self) -> lxml.etree._Element:
        namespaces = self._xml_document.getroot().nsmap
        return self._xml_document.xpath("./office:body/office:text", namespaces = namespaces)[0] # type: ignore


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

        for text_index, text_element in enumerate(heading_element.enumerate_text()):
            self.add_text(heading_as_xml, text_element)

            if text_index == 0 and self.heading_prefix_style is not None:
                if self.heading_prefix_style in text_element.style_collection:
                    self._create_line_break_element(heading_as_xml)


    def add_paragraph(self, paragraph_element: ParagraphElement) -> None:
        paragraph_as_xml = self._create_text_xml_element(None, "p", paragraph_element.style_collection, None)

        for text_element in paragraph_element.enumerate_text():
            self.add_text(paragraph_as_xml, text_element)


    def add_text(self, paragraph_as_xml: lxml.etree._Element, text_element: TextElement) -> None:
        self._create_text_xml_element(paragraph_as_xml, "span", text_element.style_collection, text_element.text)


    def _create_text_xml_element(self,
            parent: Optional[lxml.etree._Element], tag: str, style_collection: List[str], text: Optional[str]) -> lxml.etree._Element:

        body_as_xml = self._get_body_text_element()
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
        body_as_xml = self._get_body_text_element()
        if parent is None:
            parent = body_as_xml

        tag = lxml.etree.QName(body_as_xml.nsmap["text"], "line-break")
        element = lxml.etree.SubElement(parent, tag)

        return element
