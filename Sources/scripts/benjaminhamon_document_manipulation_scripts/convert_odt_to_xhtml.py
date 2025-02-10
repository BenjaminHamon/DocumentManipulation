# cspell:words fodt lxml

import argparse
import os
import re
import shutil
from typing import List, Optional

import lxml.etree

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.epub.epub_xhtml_writer import EpubXhtmlWriter
from benjaminhamon_document_manipulation_toolkit.open_document.odt_reader import OdtReader
from benjaminhamon_document_manipulation_toolkit.open_document.odt_to_document_converter import OdtToDocumentConverter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    convert_odt_to_xhtml(
        serializer = create_serializer(os.path.splitext(arguments.style_sheet)[1].lstrip(".") if arguments.style_sheet is not None else "yaml"),
        source_file_path_collection = [ os.path.normpath(path) for path in arguments.source ],
        destination_directory = os.path.normpath(arguments.output),
        template_file_path = os.path.normpath(arguments.template) if arguments.template is not None else None,
        style_sheet_file_path = os.path.normpath(arguments.style_sheet) if arguments.template is not None else None,
        style_map_file_path = arguments.style_map,
        section_regex = arguments.section_regex,
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description = "Convert odt files to xhtml.")
    argument_parser.add_argument("--source", required = True, nargs = "+", metavar = "<path>", help = "paths to the odt or fodt files to use as the source")
    argument_parser.add_argument("--output", required = True, metavar = "<path>", help = "path to the directory where to create the new xhtml files")
    argument_parser.add_argument("--template", metavar = "<path>", help = "path to the xhtml file to use as the template")
    argument_parser.add_argument("--style-sheet", metavar = "<path>", help = "path to the css file for the new xhtml files")
    argument_parser.add_argument("--style-map", metavar = "<path>", help = "path to the yaml file for a style conversion map")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the destination if it exists")
    argument_parser.add_argument("--section-regex", metavar = "<regex>", help = "filter the content based on section title")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    return serializer_factory.create_serializer(serialization_type)


def convert_odt_to_xhtml( # pylint: disable = too-many-arguments
        serializer: Serializer,
        source_file_path_collection: List[str],
        destination_directory: str,
        style_sheet_file_path: Optional[str] = None,
        section_regex: Optional[str] = None,
        template_file_path: Optional[str] = None,
        style_map_file_path: Optional[str] = None,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if len(source_file_path_collection) == 0:
        raise ValueError("Source file path collection must not be empty")

    if os.path.exists(destination_directory):
        if not overwrite:
            raise RuntimeError("Destination already exists: '%s'" % destination_directory)

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(OdtToDocumentConverter(), xml_parser)
    xhtml_writer = EpubXhtmlWriter()

    document_content = read_source(odt_reader, source_file_path_collection, section_regex)

    if style_map_file_path is not None:
        convert_styles(serializer, document_content, style_map_file_path)

    if not simulate:
        if os.path.exists(destination_directory):
            shutil.rmtree(destination_directory)
        os.makedirs(destination_directory)

    xhtml_writer.write_as_many_documents(destination_directory, document_content,
        template_file_path = template_file_path, css_file_path = style_sheet_file_path, simulate = simulate)


def read_source(odt_reader: OdtReader, source_file_path_collection: List[str], section_regex: Optional[str] = None) -> RootElement:
    document_content: Optional[RootElement] = None

    for source_file_path in source_file_path_collection:
        new_document_content = odt_reader.read_content_from_file(source_file_path)

        if document_content is None:
            document_content = new_document_content
        else:
            document_content.children += new_document_content.children

    if document_content is None:
        raise RuntimeError("Document content should not be null here")

    if section_regex is not None:
        for section in list(document_content.enumerate_sections()):
            section_title_match = re.search(section_regex, section.get_heading().get_title())
            if section_title_match is None:
                document_content.children.remove(section)

    return document_content


def convert_styles(serializer: Serializer, document_content: RootElement, style_map_file_path: str) -> None:
    style_map_configuration: dict = serializer.deserialize_from_file(style_map_file_path, dict)
    style_map = { style["odt"]: style["css"] for style in style_map_configuration["style_collection"] }

    document_operations.convert_styles(document_content, style_map)


if __name__ == "__main__":
    main()
