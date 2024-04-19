# cspell:words lxml nsmap

from typing import Dict, List, Optional

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.documents.text_region_end_element import TextRegionEndElement
from benjaminhamon_document_manipulation_toolkit.documents.text_region_start_element import TextRegionStartElement
from benjaminhamon_document_manipulation_toolkit.open_document import odt_operations


class OdtBuilder:


    def __init__(self, xml_document_base: lxml.etree._ElementTree) -> None:
        self._xml_document = xml_document_base


    def get_xml_document(self) -> lxml.etree._ElementTree:
        return self._xml_document


    def add_content(self, root_element: RootElement, comment_collection: Dict[str,DocumentComment]) -> None:
        for section_element in root_element.enumerate_sections():
            self.add_section(section_element, comment_collection)


    def add_section(self, section_element: SectionElement, comment_collection: Dict[str,DocumentComment]) -> None:
        self.add_heading(section_element.get_heading(), comment_collection)

        for paragraph in section_element.enumerate_paragraphs():
            self.add_paragraph(paragraph, comment_collection)

        for subsection in section_element.enumerate_subsections():
            self.add_section(subsection, comment_collection)


    def add_heading(self, heading_element: HeadingElement, comment_collection: Dict[str,DocumentComment]) -> None:
        heading_as_xml = self._create_text_xml_element(None, "h", heading_element.style_collection, None)

        for child in heading_element.children:
            if isinstance(child, TextElement):
                self.add_text(heading_as_xml, child)
            if isinstance(child, TextRegionStartElement):
                comment = self._get_comment_for_region(child, comment_collection)
                self._create_annotation_xml_element(heading_as_xml, child, comment)
            if isinstance(child, TextRegionEndElement):
                self._create_annotation_end_xml_element(heading_as_xml, child)


    def add_paragraph(self, paragraph_element: ParagraphElement, comment_collection: Dict[str,DocumentComment]) -> None:
        paragraph_as_xml = self._create_text_xml_element(None, "p", paragraph_element.style_collection, None)

        for child in paragraph_element.children:
            if isinstance(child, TextElement):
                self.add_text(paragraph_as_xml, child)
            if isinstance(child, TextRegionStartElement):
                comment = self._get_comment_for_region(child, comment_collection)
                self._create_annotation_xml_element(paragraph_as_xml, child, comment)
            if isinstance(child, TextRegionEndElement):
                self._create_annotation_end_xml_element(paragraph_as_xml, child)


    def add_text(self, paragraph_as_xml: lxml.etree._Element, text_element: TextElement) -> None:
        self._create_text_xml_element(paragraph_as_xml, "span", text_element.style_collection, text_element.text)
        if text_element.line_break:
            self._create_line_break_element(paragraph_as_xml)


    def _create_text_xml_element(self,
            parent: Optional[lxml.etree._Element], tag: str, style_collection: List[str], text: Optional[str]) -> lxml.etree._Element:

        namespaces = self._xml_document.getroot().nsmap

        if parent is None:
            parent = odt_operations.get_body_text_element(self._xml_document)

        attributes: Dict[str,str] = {}
        if len(style_collection) > 1:
            raise ValueError("Too many styles")
        if len(style_collection) == 1:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style_collection[0]

        element = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["text"], tag), attrib = attributes)
        element.text = text

        return element


    def _create_line_break_element(self, parent: Optional[lxml.etree._Element]) -> lxml.etree._Element:
        namespaces = self._xml_document.getroot().nsmap

        if parent is None:
            parent = odt_operations.get_body_text_element(self._xml_document)

        tag = lxml.etree.QName(namespaces["text"], "line-break")
        element = lxml.etree.SubElement(parent, tag)

        return element


    def _create_annotation_xml_element(self,
            paragraph_as_xml: lxml.etree._Element, region_start_element: TextRegionStartElement, comment: DocumentComment) -> None:

        namespaces = self._xml_document.getroot().nsmap

        if region_start_element.identifier is None:
            raise ValueError("Region element must have an identifier")

        attributes: Dict[str,str] = {}
        attributes[str(lxml.etree.QName(namespaces["office"], "name"))] = region_start_element.identifier
        comment_as_xml = lxml.etree.SubElement(paragraph_as_xml, lxml.etree.QName(namespaces["office"], "annotation"), attrib = attributes)

        lxml.etree.SubElement(comment_as_xml, lxml.etree.QName(namespaces["dc"], "creator")).text = comment.author
        lxml.etree.SubElement(comment_as_xml, lxml.etree.QName(namespaces["dc"], "date")).text = comment.date.isoformat()

        for text_paragraph in comment.text.splitlines():
            self._create_text_xml_element(comment_as_xml, "p", [], text_paragraph)


    def _create_annotation_end_xml_element(self, paragraph_as_xml: lxml.etree._Element, region_end_element: TextRegionEndElement) -> None:
        namespaces = self._xml_document.getroot().nsmap

        if region_end_element.identifier is None:
            raise ValueError("Region element must have an identifier")

        attributes: Dict[str,str] = {}
        attributes[str(lxml.etree.QName(namespaces["office"], "name"))] = region_end_element.identifier
        lxml.etree.SubElement(paragraph_as_xml, lxml.etree.QName(namespaces["office"], "annotation-end"), attrib = attributes)


    def _get_comment_for_region(self, region_start_element: TextRegionStartElement, comment_collection: Dict[str,DocumentComment]) -> DocumentComment:
        if region_start_element.identifier is None:
            raise ValueError("Region element must have an identifier")
        return comment_collection[region_start_element.identifier]
