from typing import Optional

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers


class EpubXhtmlBuilder:


    def __init__(self, title: str, template_file_path: Optional[str] = None) -> None:
        self._xhtml_document = EpubXhtmlBuilder._create_document(title, template_file_path)


    @staticmethod
    def _create_document(title: str, template_file_path: Optional[str] = None) -> lxml.etree._ElementTree:
        if template_file_path is None:
            document = epub_xhtml_helpers.create_xhtml()
        else:
            document = epub_xhtml_helpers.load_xhtml(template_file_path)

        root = document.getroot()

        title_element = epub_xhtml_helpers.try_find_xhtml_element(root, "./x:head/x:title")
        if title_element is None:
            head_element = epub_xhtml_helpers.find_xhtml_element(root, "./x:head")
            title_element = epub_xhtml_helpers.create_xhtml_subelement(head_element, "title")

        title_element.text = title

        return document


    def get_xhtml_document(self) -> lxml.etree._ElementTree:
        return self._xhtml_document


    def add_content(self, root_element: RootElement) -> None:
        body_as_xml = epub_xhtml_helpers.find_xhtml_element(self._xhtml_document.getroot(), "./x:body")
        for section_element in root_element.enumerate_sections():
            self.add_section(body_as_xml, section_element, level = 1)


    def add_content_from_section(self, section_element: SectionElement) -> None:
        body_as_xml = epub_xhtml_helpers.find_xhtml_element(self._xhtml_document.getroot(), "./x:body")
        self.add_section(body_as_xml, section_element, level = 1)


    def add_section(self, xhtml_element: lxml.etree._Element, section_element: SectionElement, level: int) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(section_element)
        section_as_html = epub_xhtml_helpers.create_xhtml_subelement(xhtml_element, "section", attributes = attributes)

        self.add_heading(section_as_html, section_element.get_heading(), level)

        for paragraph in section_element.enumerate_paragraphs():
            self.add_paragraph(section_as_html, paragraph)

        for subsection in section_element.enumerate_subsections():
            self.add_section(section_as_html, subsection, level + 1)

        return section_as_html


    def add_heading(self, xhtml_element: lxml.etree._Element, heading_element: HeadingElement, level: int) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(heading_element)
        heading_as_html = epub_xhtml_helpers.create_xhtml_subelement(xhtml_element, "h" + str(level), attributes = attributes)

        for text_element in heading_element.enumerate_text():
            self.add_text(heading_as_html, text_element)

        return heading_as_html


    def add_paragraph(self, xhtml_element: lxml.etree._Element, paragraph_element: ParagraphElement) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(paragraph_element)
        paragraph_as_html = epub_xhtml_helpers.create_xhtml_subelement(xhtml_element, "p", attributes = attributes)

        for text_element in paragraph_element.enumerate_text():
            self.add_text(paragraph_as_html, text_element)

        if len(paragraph_element.children) == 0:
            paragraph_as_html.text = "\u00a0" # no-break space

        return paragraph_as_html


    def add_text(self, xhtml_element: lxml.etree._Element, text_element: TextElement) -> lxml.etree._Element:
        attributes = self._get_html_attributes_from_element(text_element)
        return epub_xhtml_helpers.create_xhtml_subelement(xhtml_element, "span", attributes = attributes, text = text_element.text)


    def _get_html_attributes_from_element(self, element: DocumentElement) -> dict:
        attributes = {}

        if element.identifier is not None:
            attributes["id"] = element.identifier
        if len(element.style_collection) > 0:
            attributes["class"] = " ".join(element.style_collection)

        return attributes
