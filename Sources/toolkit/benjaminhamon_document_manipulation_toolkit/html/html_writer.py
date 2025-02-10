# cspell:words lxml

import logging
import os
from typing import Mapping, Optional

import lxml.etree
import lxml.html.html5parser

from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.html import html_operations
from benjaminhamon_document_manipulation_toolkit.html.document_to_html_converter import DocumentToHtmlConverter
from benjaminhamon_document_manipulation_toolkit.xml import xml_operations, xpath_helpers


logger = logging.getLogger("HtmlWriter")


class HtmlWriter:


    def __init__(self, converter: DocumentToHtmlConverter, parser: lxml.html.html5parser.HTMLParser) -> None:
        self._converter = converter
        self._parser = parser
        self.pretty_print = True
        self.encoding = "utf-8"


    def write_to_file(self, output_file_path: str, document_as_html: lxml.etree._ElementTree, simulate: bool = False) -> None:
        logger.debug("Writing '%s'", output_file_path)

        write_options = {
            "encoding": self.encoding,
            "pretty_print": self.pretty_print,
            "doctype": "<!doctype html>",
        }

        # lxml.html.tostring exists but creates link elements which are not closed.
        document_as_html_string: str = lxml.etree.tostring(document_as_html, **write_options).decode(self.encoding)

        if not simulate:
            if self.pretty_print:
                # lxml.html.html5parser.HTMLParser does not have the remove_blank_text option, which causes the pretty_print to produce garbage.
                # To work around that we parse the XML again through the base lxml parser.
                parser = lxml.etree.XMLParser(remove_blank_text = True)
                document_as_html_string = "\n".join(document_as_html_string.splitlines()[1:])
                document_reloaded = lxml.etree.fromstring(document_as_html_string, parser)
                document_as_html_string = lxml.etree.tostring(document_reloaded, **write_options).decode(self.encoding)

            with open(output_file_path + ".tmp", mode = "w", encoding = self.encoding) as output_file:
                output_file.write(document_as_html_string)
            os.replace(output_file_path + ".tmp", output_file_path)


    def write_as_single_document(self, # pylint: disable = too-many-arguments
            output_file_path: str, title: str, metadata: Mapping[str,str], document_content: RootElement,
            template_file_path: Optional[str] = None, css_file_path: Optional[str] = None, simulate: bool = False) -> None:

        html_document = self._create_document(title, output_file_path, template_file_path, css_file_path)
        html_document = self._converter.convert(html_document, title, metadata, document_content)

        self.write_to_file(output_file_path, html_document, simulate = simulate)


    def write_as_many_documents(self, # pylint: disable = too-many-arguments
            output_directory: str,
            metadata: Mapping[str,str],
            document_content: RootElement,
            section_template_file_path: Optional[str] = None,
            information_template_file_path: Optional[str] = None,
            css_file_path: Optional[str] = None,
            simulate: bool = False,
            ) -> None:

        section_count = document_content.get_section_count()

        if information_template_file_path is not None:
            section_index = -1
            file_name = document_operations.generate_section_file_name("Information", section_index, section_count)
            output_file_path = os.path.join(output_directory, file_name + ".html")
            self.write_metadata(output_file_path, metadata, information_template_file_path, css_file_path, simulate = simulate)

        for section_index, section in enumerate(document_content.enumerate_sections()):
            title = section.get_heading().get_title()

            file_name = document_operations.generate_section_file_name(title, section_index, section_count)
            output_file_path = os.path.join(output_directory, file_name + ".html")

            html_document = self._create_document(title, output_file_path, section_template_file_path, css_file_path)
            html_document = self._converter.convert_as_section(html_document, section)

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
            destination_file_path: str,
            template_file_path: Optional[str],
            css_file_path: Optional[str],
            ) -> lxml.etree._ElementTree:

        def create_base():
            if template_file_path is not None:
                with open(template_file_path, mode = "r", encoding = "utf-8") as template_file:
                    return self._parser.parse(template_file)

            html_root = lxml.etree.Element("html")
            head_as_html = lxml.etree.SubElement(html_root, "head")
            lxml.etree.SubElement(head_as_html, "title")
            lxml.etree.SubElement(html_root, "body")
            return lxml.etree.ElementTree(html_root)

        html_document = create_base()
        html_root = html_document.getroot()
        head_as_html = xpath_helpers.find_xml_element(html_root, "./head")
        title_as_html = xpath_helpers.find_xml_element(html_root, "./head/title")
        title_as_html.text = title
        body_as_html = xpath_helpers.find_xml_element(html_root, "./body")
        body_as_html.text = None

        if template_file_path is not None:
            for link_element in xpath_helpers.try_find_xml_element_collection(html_root, "//link"):
                html_operations.update_link(link_element, template_file_path, destination_file_path)
        if css_file_path is not None:
            html_operations.add_style_sheet(head_as_html, "link", css_file_path, destination_file_path)

        return html_document
