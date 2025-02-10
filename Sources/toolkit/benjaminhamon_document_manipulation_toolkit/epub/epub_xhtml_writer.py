# cspell:words lxml nsmap

import logging
import os
from typing import Mapping, Optional

import lxml.etree
import lxml.html

from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_document_manipulation_toolkit.epub.document_to_xhtml_converter import DocumentToXhtmlConverter
from benjaminhamon_document_manipulation_toolkit.html import html_operations
from benjaminhamon_document_manipulation_toolkit.xml import xml_operations


logger = logging.getLogger("EpubXhtmlWriter")


# Implementation is close to HtmlWriter, but since there is a large number of small changes, we don't inherit from it.

class EpubXhtmlWriter:


    def __init__(self, converter: DocumentToXhtmlConverter, parser: lxml.html.XHTMLParser) -> None:
        self._converter = converter
        self._parser = parser
        self.pretty_print = True
        self.encoding = "utf-8"


    def write_to_file(self, output_file_path: str, document_as_html: lxml.etree._ElementTree, simulate: bool = False) -> None:
        logger.debug("Writing '%s'", output_file_path)

        write_options = {
            "encoding": self.encoding,
            "pretty_print": self.pretty_print,
            "doctype": "<?xml version=\"1.0\" encoding=\"%s\"?>" % self.encoding,
        }

        # lxml.html.tostring exists but creates link elements which are not closed.
        document_as_html_string: str = lxml.etree.tostring(document_as_html, **write_options).decode(self.encoding)

        if not simulate:
            with open(output_file_path + ".tmp", mode = "w", encoding = self.encoding) as output_file:
                output_file.write(document_as_html_string)
            os.replace(output_file_path + ".tmp", output_file_path)


    def write_as_single_document(self, # pylint: disable = too-many-arguments
            output_file_path: str, title: str, content: RootElement,
            template_file_path: Optional[str] = None, css_file_path: Optional[str] = None, simulate: bool = False) -> None:

        html_document = self._create_document(title, output_file_path, template_file_path, css_file_path)
        html_document = self._converter.convert(html_document, content)

        self.write_to_file(output_file_path, html_document, simulate = simulate)


    def write_as_many_documents(self, # pylint: disable = too-many-arguments, too-many-locals
            output_directory: str,
            metadata: Mapping[str,str],
            content: RootElement,
            section_template_file_path: Optional[str] = None,
            information_template_file_path: Optional[str] = None,
            css_file_path: Optional[str] = None,
            simulate: bool = False) -> None:

        section_count = content.get_section_count()

        if information_template_file_path is not None:
            section_index = -1
            file_name = document_operations.generate_section_file_name("Information", section_index, section_count)
            output_file_path = os.path.join(output_directory, file_name + ".xhtml")
            self.write_metadata(output_file_path, metadata, information_template_file_path, simulate = simulate)

        for section_index, section in enumerate(content.enumerate_sections()):
            section_root = RootElement()
            section_root.children.append(section)
            title = section.get_heading().get_title()

            file_name = document_operations.generate_section_file_name(title, section_index, section_count)
            output_file_path = os.path.join(output_directory, file_name + ".xhtml")

            html_document = self._create_document(title, output_file_path, section_template_file_path, css_file_path)
            html_document = self._converter.convert(html_document, section_root)

            self.write_to_file(output_file_path, html_document, simulate = simulate)


    def write_metadata(self, # pylint: disable = too-many-arguments
            output_file_path: str,
            metadata: Mapping[str,str],
            template_file_path: str,
            css_file_path: Optional[str] = None,
            simulate: bool = False) -> None:

        html_document = self._create_document("Information", output_file_path, template_file_path, css_file_path)
        xml_operations.format_text_in_xml(html_document.getroot(), metadata)
        self.write_to_file(output_file_path, html_document, simulate = simulate)


    def _create_document(self,
            title: str,
            output_file_path: str,
            template_file_path: Optional[str],
            css_file_path: Optional[str],
            ) -> lxml.etree._ElementTree:

        html_document = epub_xhtml_helpers.create_xhtml_base(title, self._parser, template_file_path)
        html_root = html_document.getroot()
        head_as_html = epub_xhtml_helpers.find_xhtml_element(html_root, "./x:head")
        body_as_html = epub_xhtml_helpers.find_xhtml_element(html_root, "./x:body")
        body_as_html.text = None

        if template_file_path is not None:
            for link_element in epub_xhtml_helpers.try_find_xhtml_element_collection(html_root, "//x:link"):
                html_operations.update_link(link_element, template_file_path, output_file_path)
        if css_file_path is not None:
            html_operations.add_style_sheet(head_as_html, str(epub_xhtml_helpers.qualify_tag("link")), css_file_path, output_file_path)

        return html_document
