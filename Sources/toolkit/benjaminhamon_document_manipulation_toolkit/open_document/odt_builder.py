# cspell:words lxml nsmap

from typing import Dict, Optional

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.document_element import DocumentElement
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
        self._add_heading_xml(odt_operations.get_body_text_element(self._xml_document), heading_element, comment_collection)


    def add_paragraph(self, paragraph_element: ParagraphElement, comment_collection: Dict[str,DocumentComment]) -> None:
        self._add_paragraph_xml(odt_operations.get_body_text_element(self._xml_document), paragraph_element, comment_collection)


    def _add_heading_xml(self,
            parent: lxml.etree._Element, heading_element: HeadingElement, comment_collection: Dict[str,DocumentComment]) -> lxml.etree._Element:

        namespaces = self._xml_document.getroot().nsmap

        attributes: Dict[str,str] = {}

        style = self._get_style_from_document_element(heading_element)
        if style is not None:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style

        heading_xml = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["text"], "h"), attrib = attributes)
        self._add_text_elements_xml(heading_xml, heading_element, comment_collection)

        return heading_xml


    def _add_paragraph_xml(self,
            parent: lxml.etree._Element, paragraph_element: ParagraphElement, comment_collection: Dict[str,DocumentComment]) -> lxml.etree._Element:

        namespaces = self._xml_document.getroot().nsmap

        attributes: Dict[str,str] = {}

        style = self._get_style_from_document_element(paragraph_element)
        if style is not None:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style

        paragraph_xml = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["text"], "p"), attrib = attributes)
        self._add_text_elements_xml(paragraph_xml, paragraph_element, comment_collection)

        return paragraph_xml


    def _add_paragraph_xml_from_str(self, parent: lxml.etree._Element, text: str) -> lxml.etree._Element:
        namespaces = self._xml_document.getroot().nsmap

        paragraph_xml = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["text"], "p"))
        paragraph_xml.text = text

        return paragraph_xml


    def _add_text_elements_xml(self,
            parent: lxml.etree._Element, document_element: DocumentElement, comment_collection: Dict[str,DocumentComment]) -> lxml.etree._Element:

        for child in document_element.children:
            if isinstance(child, TextElement):
                self._add_span_xml(parent, child)

            if isinstance(child, TextRegionStartElement):
                if child.identifier is None:
                    raise ValueError("Region element must have an identifier")
                comment = comment_collection.get(child.identifier)
                if comment is not None:
                    self._add_annotation_xml(parent, child, comment)

            if isinstance(child, TextRegionEndElement):
                self._add_annotation_end_xml(parent, child)

        return parent


    def _add_span_xml(self, parent: lxml.etree._Element, text_element: TextElement) -> lxml.etree._Element:
        namespaces = self._xml_document.getroot().nsmap

        attributes: Dict[str,str] = {}

        style = self._get_style_from_document_element(text_element)
        if style is not None:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style

        span_xml = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["text"], "span"), attrib = attributes)
        span_xml.text = text_element.text

        if text_element.line_break:
            self._add_line_break_xml(parent)

        return span_xml


    def _add_line_break_xml(self, parent: lxml.etree._Element) -> lxml.etree._Element:
        namespaces = self._xml_document.getroot().nsmap

        tag = lxml.etree.QName(namespaces["text"], "line-break")
        line_break_xml = lxml.etree.SubElement(parent, tag)

        return line_break_xml


    def _add_annotation_xml(self,
            parent: lxml.etree._Element, region_start_element: TextRegionStartElement, comment: DocumentComment) -> lxml.etree._Element:

        namespaces = self._xml_document.getroot().nsmap

        if region_start_element.identifier is None:
            raise ValueError("Region element must have an identifier")

        attributes: Dict[str,str] = {}
        attributes[str(lxml.etree.QName(namespaces["office"], "name"))] = region_start_element.identifier
        annotation_xml = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["office"], "annotation"), attrib = attributes)

        lxml.etree.SubElement(annotation_xml, lxml.etree.QName(namespaces["dc"], "creator")).text = comment.author
        lxml.etree.SubElement(annotation_xml, lxml.etree.QName(namespaces["dc"], "date")).text = comment.date.isoformat()

        for text_paragraph in comment.text.splitlines():
            self._add_paragraph_xml_from_str(annotation_xml, text_paragraph)

        return annotation_xml


    def _add_annotation_end_xml(self, parent: lxml.etree._Element, region_end_element: TextRegionEndElement) -> lxml.etree._Element:
        namespaces = self._xml_document.getroot().nsmap

        if region_end_element.identifier is None:
            raise ValueError("Region element must have an identifier")

        attributes: Dict[str,str] = {}
        attributes[str(lxml.etree.QName(namespaces["office"], "name"))] = region_end_element.identifier
        annotation_end_xml = lxml.etree.SubElement(parent, lxml.etree.QName(namespaces["office"], "annotation-end"), attrib = attributes)

        return annotation_end_xml


    def _get_style_from_document_element(self, document_element: DocumentElement) -> Optional[str]:
        if len(document_element.style_collection) > 1:
            raise ValueError("Too many styles")
        if len(document_element.style_collection) == 1:
            return document_element.style_collection[0]
        return None
