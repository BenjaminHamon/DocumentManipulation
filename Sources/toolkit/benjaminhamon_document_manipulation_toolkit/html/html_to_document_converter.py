# cspell:words lxml

from typing import List

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.elements.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.xml import xpath_helpers


class HtmlToDocumentConverter:


    def convert_content(self, document_as_xml: lxml.etree._Element) -> RootElement:
        body_as_xml = xpath_helpers.find_xml_element(document_as_xml, "body")

        root_element = RootElement()
        root_element.identifier = "root"

        section_collection_as_xml = xpath_helpers.try_find_xml_element_collection(body_as_xml, "section")
        for section_as_xml in section_collection_as_xml:
            root_element.children.append(self._convert_section(section_as_xml))

        return root_element


    def _convert_section(self, section_as_xml: lxml.etree._Element) -> SectionElement:
        section_element = SectionElement()

        heading_as_xml = xpath_helpers.try_find_xml_element(section_as_xml, "*[self::h1 or self::h2 or self::h3]")

        if heading_as_xml is not None and heading_as_xml.text is not None:
            heading_element = HeadingElement()
            text_element = TextElement(heading_as_xml.text)
            heading_element.children.append(text_element)
            section_element.children.append(heading_element)

        paragraph_collection_as_xml = xpath_helpers.try_find_xml_element_collection(section_as_xml, "p")
        for paragraph_as_xml in paragraph_collection_as_xml:
            section_element.children.append(self._convert_paragraph(paragraph_as_xml))

        subsection_collection_as_xml = xpath_helpers.try_find_xml_element_collection(section_as_xml, "section")
        for subsection_as_xml in subsection_collection_as_xml:
            section_element.children.append(self._convert_section(subsection_as_xml))


        return section_element


    def _convert_paragraph(self, paragraph_as_xml: lxml.etree._Element) -> ParagraphElement:
        paragraph_element = ParagraphElement()

        if paragraph_as_xml.text is not None:
            text_element = TextElement(paragraph_as_xml.text)
            paragraph_element.children.append(text_element)

        paragraph_element.style_collection = self._get_styles_from_element(paragraph_as_xml)

        span_collection_as_xml = xpath_helpers.try_find_xml_element_collection(paragraph_as_xml, "span")

        for span_as_xml in span_collection_as_xml:
            if span_as_xml.text is not None:
                text_element = TextElement(span_as_xml.text)
                text_element.style_collection = self._get_styles_from_element(span_as_xml)
                paragraph_element.children.append(text_element)

            if span_as_xml.tail is not None:
                text_element = TextElement(span_as_xml.tail)
                paragraph_element.children.append(text_element)

        return paragraph_element


    def _get_styles_from_element(self, element_as_xml: lxml.etree._Element) -> List[str]:
        class_attribute = element_as_xml.attrib.get("class")
        if class_attribute is not None:
            return class_attribute.split(" ")

        return []
