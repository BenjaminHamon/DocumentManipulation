# cspell:words lxml nsmap

from typing import Dict, List, Optional

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents import document_element_factory
from benjaminhamon_document_manipulation_toolkit.documents.elements.document_comment import DocumentComment
from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_region_end_element import TextRegionEndElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_region_start_element import TextRegionStartElement
from benjaminhamon_document_manipulation_toolkit.xml import xpath_helpers


class DocumentToOdtConverter:


    def convert(self,
            xml_document: lxml.etree._ElementTree,
            content: RootElement,
            comment_collection: Dict[str,DocumentComment]) -> lxml.etree._ElementTree:

        namespaces = xpath_helpers.sanitize_namespaces_for_xpath(xml_document.getroot().nsmap)
        body_as_xml = xpath_helpers.find_xml_element(xml_document.getroot(), "./office:body/office:text", namespaces)

        xml_element_collection: List[lxml.etree._Element] = []
        for section_element in content.enumerate_sections():
            xml_element_collection.extend(self._convert_section(section_element, comment_collection, namespaces))

        for xml_element in xml_element_collection:
            body_as_xml.append(xml_element)

        return xml_document


    def _convert_section(self,
            section_element: SectionElement, comment_collection: Dict[str,DocumentComment], namespaces: Dict[str, str]) -> List[lxml.etree._Element]:

        xml_element_collection: List[lxml.etree._Element] = []

        xml_element_collection.append(self._convert_heading(section_element.get_heading(), comment_collection, namespaces))
        for paragraph in section_element.enumerate_paragraphs():
            xml_element_collection.append(self._convert_paragraph(paragraph, comment_collection, namespaces))
        for subsection in section_element.enumerate_subsections():
            xml_element_collection.extend(self._convert_section(subsection, comment_collection, namespaces))

        return xml_element_collection


    def _convert_heading(self,
            heading_element: HeadingElement, comment_collection: Dict[str,DocumentComment], namespaces: Dict[str, str]) -> lxml.etree._Element:

        attributes: Dict[str,str] = {}

        style = self._get_style_from_document_element(heading_element)
        if style is not None:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style

        heading_as_xml = lxml.etree.Element(lxml.etree.QName(namespaces["text"], "h"), attrib = attributes)
        for child in heading_element.children:
            new_elements = self._convert_text(child, comment_collection, namespaces)
            for element in new_elements:
                heading_as_xml.append(element)

        return heading_as_xml


    def _convert_paragraph(self,
            paragraph_element: ParagraphElement,
            comment_collection: Optional[Dict[str,DocumentComment]],
            namespaces: Dict[str, str],
            ) -> lxml.etree._Element:

        attributes: Dict[str,str] = {}

        style = self._get_style_from_document_element(paragraph_element)
        if style is not None:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style

        paragraph_as_xml = lxml.etree.Element(lxml.etree.QName(namespaces["text"], "p"), attrib = attributes)
        for child in paragraph_element.children:
            new_elements = self._convert_text(child, comment_collection, namespaces)
            for element in new_elements:
                paragraph_as_xml.append(element)

        return paragraph_as_xml


    def _convert_text(self,
            element: DocumentElement,
            comment_collection: Optional[Dict[str,DocumentComment]],
            namespaces: Dict[str, str],
            ) -> List[lxml.etree._Element]:

        xml_element_collection: List[lxml.etree._Element] = []

        if isinstance(element, TextElement):
            xml_element_collection.append(self._convert_text_span(element, namespaces))
            if element.line_break:
                xml_element_collection.append(self._create_line_break(namespaces))
            return xml_element_collection

        if isinstance(element, TextRegionStartElement):
            if element.identifier is None:
                raise ValueError("Region element must have an identifier")
            if comment_collection is not None:
                comment = comment_collection.get(element.identifier)
                if comment is not None:
                    xml_element_collection.append(self._convert_annotation(element, comment, namespaces))
            return xml_element_collection

        if isinstance(element, TextRegionEndElement):
            if element.identifier is None:
                raise ValueError("Region element must have an identifier")
            if comment_collection is not None:
                comment = comment_collection.get(element.identifier)
                if comment is not None:
                    xml_element_collection.append(self._convert_annotation_end(element, namespaces))
            return xml_element_collection

        raise ValueError("Unsupported element type: '%s'" % type(element))


    def _convert_text_span(self, text_element: TextElement, namespaces: Dict[str, str]) -> lxml.etree._Element:
        attributes: Dict[str,str] = {}

        style = self._get_style_from_document_element(text_element)
        if style is not None:
            attributes[str(lxml.etree.QName(namespaces["text"], "style-name"))] = style

        span_as_xml = lxml.etree.Element(lxml.etree.QName(namespaces["text"], "span"), attrib = attributes)
        span_as_xml.text = text_element.text

        return span_as_xml


    def _create_line_break(self, namespaces: Dict[str, str]) -> lxml.etree._Element:
        return lxml.etree.Element(lxml.etree.QName(namespaces["text"], "line-break"))


    def _convert_annotation(self,
            region_start_element: TextRegionStartElement, comment: DocumentComment, namespaces: Dict[str, str]) -> lxml.etree._Element:

        if region_start_element.identifier is None:
            raise ValueError("Region element must have an identifier")

        attributes: Dict[str,str] = {}
        if region_start_element.identifier.startswith("__Annotation__"):
            attributes[str(lxml.etree.QName(namespaces["office"], "name"))] = region_start_element.identifier
        annotation_xml = lxml.etree.Element(lxml.etree.QName(namespaces["office"], "annotation"), attrib = attributes)

        lxml.etree.SubElement(annotation_xml, lxml.etree.QName(namespaces["dc"], "creator")).text = comment.author
        lxml.etree.SubElement(annotation_xml, lxml.etree.QName(namespaces["dc"], "date")).text = comment.date.isoformat()

        for paragraph_text in comment.text.splitlines():
            paragraph_element = document_element_factory.create_paragraph([ paragraph_text ])
            annotation_xml.append(self._convert_paragraph(paragraph_element, comment_collection = None, namespaces = namespaces))

        return annotation_xml


    def _convert_annotation_end(self, region_end_element: TextRegionEndElement, namespaces: Dict[str, str]) -> lxml.etree._Element:
        if region_end_element.identifier is None:
            raise ValueError("Region element must have an identifier")

        attributes: Dict[str,str] = {}
        attributes[str(lxml.etree.QName(namespaces["office"], "name"))] = region_end_element.identifier
        annotation_end_xml = lxml.etree.Element(lxml.etree.QName(namespaces["office"], "annotation-end"), attrib = attributes)

        return annotation_end_xml


    def _get_style_from_document_element(self, document_element: DocumentElement) -> Optional[str]:
        if len(document_element.style_collection) > 1:
            raise ValueError("Too many styles")
        if len(document_element.style_collection) == 1:
            return document_element.style_collection[0]
        return None
