# cspell:words fodt lxml postprocess

import logging
import os
import re
from typing import Optional
import zipfile

import lxml.etree

from benjaminhamon_book_distribution_toolkit.documents import document_operations
from benjaminhamon_book_distribution_toolkit.documents.root_element import RootElement
from benjaminhamon_book_distribution_toolkit.open_document import odt_operations
from benjaminhamon_book_distribution_toolkit.open_document.odt_builder import OdtBuilder


logger = logging.getLogger("OdtWriter")


class OdtWriter:


    def __init__(self, xml_parser: lxml.etree.XMLParser) -> None:
        self._xml_parser = xml_parser

        self.pretty_print = True
        self.encoding = "utf-8"
        self.heading_prefix_style: Optional[str] = None


    def write_to_file(self, output_file_path: str, document: lxml.etree._ElementTree, flat_odt: bool = False, simulate: bool = False) -> None:
        logger.debug("Writing '%s'", output_file_path)

        write_options = {
            "doctype": "<?xml version=\"1.0\" encoding=\"%s\"?>" % self.encoding,
            "encoding": self.encoding,
            "pretty_print": self.pretty_print,
        }

        document_as_xml_string = lxml.etree.tostring(document, **write_options).decode(self.encoding)
        document_as_xml_string = re.sub(r"/text:span>\s+<text:span", "/text:span> <text:span", document_as_xml_string)
        document_as_xml_string = re.sub(r">\s+<text:line-break/>\s+<", "><text:line-break/><", document_as_xml_string)

        if flat_odt:
            if not simulate:
                with open(output_file_path + ".tmp", mode = "w", encoding = self.encoding) as output_file:
                    output_file.write(document_as_xml_string)
                os.replace(output_file_path + ".tmp", output_file_path)

        else:
            if not simulate:
                with zipfile.ZipFile(output_file_path + ".tmp", mode = "w") as output_file:
                    output_file.writestr("content.xml", document_as_xml_string)
                os.replace(output_file_path + ".tmp", output_file_path)


    def write_as_single_document(self, # pylint: disable = too-many-arguments
            output_file_path: str, document_content: RootElement,
            template_file_path: Optional[str] = None, flat_odt: bool = False, simulate: bool = False) -> None:

        odt_builder = OdtBuilder(self._create_document(template_file_path))
        odt_builder.heading_prefix_style = self.heading_prefix_style
        odt_builder.add_content(document_content)

        self.write_to_file(output_file_path, odt_builder.get_xml_document(), flat_odt = flat_odt, simulate = simulate)


    def write_as_many_documents(self, # pylint: disable = too-many-arguments
            output_directory: str, document_content: RootElement,
            template_file_path: Optional[str] = None, flat_odt: bool = False, simulate: bool = False) -> None:

        section_count = document_content.get_section_count()

        for section_index, section in enumerate(document_content.enumerate_sections()):
            title = section.get_heading().get_title()

            odt_builder = OdtBuilder(self._create_document(template_file_path))
            odt_builder.heading_prefix_style = self.heading_prefix_style
            odt_builder.add_section(section)

            file_name = document_operations.generate_section_file_name(title, section_index, section_count)
            odt_file_path = os.path.join(output_directory, file_name + (".fodt" if flat_odt else ".odt"))

            self.write_to_file(odt_file_path, odt_builder.get_xml_document(), flat_odt = flat_odt, simulate = simulate)


    def _create_document(self, template_file_path: Optional[str]) -> lxml.etree._ElementTree:
        if template_file_path is None:
            return odt_operations.create_document()
        return odt_operations.load_document(self._xml_parser, template_file_path)
