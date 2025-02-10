# cspell:words fodt lxml

import argparse
import os
from typing import Optional

import lxml.etree
import lxml.html.html5parser

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.conversion.markdown_to_odt_configuration import MarkdownToOdtConfiguration
from benjaminhamon_document_manipulation_toolkit.conversion.serialization import markdown_to_odt_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.documents.document_definition import DocumentDefinition
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.serialization import document_definition_serialization_converter
from benjaminhamon_document_manipulation_toolkit.html.html_reader import HtmlReader
from benjaminhamon_document_manipulation_toolkit.html.html_to_document_converter import HtmlToDocumentConverter
from benjaminhamon_document_manipulation_toolkit.interfaces.document_reader import DocumentReader
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_reader import MarkdownReader
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_to_html_converter import MarkdownToHtmlConverter
from benjaminhamon_document_manipulation_toolkit.open_document.document_to_odt_converter import DocumentToOdtConverter
from benjaminhamon_document_manipulation_toolkit.open_document.odt_writer import OdtWriter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    if arguments.definition is None and arguments.source is None:
        raise ValueError("Exactly one of 'definition' and 'source' should be set")
    if arguments.definition is not None and arguments.source is not None:
        raise ValueError("Exactly one of 'definition' and 'source' should be set")

    convert_markdown_to_odt(
        serializer = create_serializer(os.path.splitext(arguments.configuration)[1].lstrip(".")),
        configuration_file_path = os.path.normpath(arguments.configuration),
        definition_file_path = os.path.normpath(arguments.definition) if arguments.definition is not None else None,
        source_file_path = os.path.normpath(arguments.source) if arguments.source is not None else None,
        destination_file_path = os.path.normpath(arguments.destination),
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(
        description = "Convert a markdown document to an odt document.")
    argument_parser.add_argument("--configuration", required = True,
        metavar = "<path>", help = "path to the conversion configuration")
    argument_parser.add_argument("--definition",
        metavar = "<path>", help = "path to the document definition (set this or source)")
    argument_parser.add_argument("--source",
        metavar = "<path>", help = "path to the markdown document (set this or definition)")
    argument_parser.add_argument("--destination", required = True,
        metavar = "<path>", help = "path to the odt document to create")
    argument_parser.add_argument("--overwrite", action = "store_true",
        help = "overwrite the destination file or directory in case it already exists")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    serializer = serializer_factory.create_serializer(serialization_type)
    serializer.add_converter(DocumentDefinition, document_definition_serialization_converter.factory())
    serializer.add_converter(MarkdownToOdtConfiguration, markdown_to_odt_configuration_serialization_converter.factory())
    return serializer


def convert_markdown_to_odt( # pylint: disable = too-many-arguments
        serializer: Serializer,
        configuration_file_path: str,
        definition_file_path: Optional[str],
        source_file_path: Optional[str],
        destination_file_path: str,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if definition_file_path is None and source_file_path is None:
        raise ValueError("Exactly one of 'definition_file_path' and 'source_file_path' must be set")
    if definition_file_path is not None and source_file_path is not None:
        raise ValueError("Exactly one of 'definition_file_path' and 'source_file_path' must be set")

    if os.path.exists(destination_file_path):
        if not overwrite:
            raise RuntimeError("Destination already exists: '%s'" % destination_file_path)

    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_reader = HtmlReader(HtmlToDocumentConverter(), html_parser)
    markdown_reader = MarkdownReader(MarkdownToHtmlConverter(), html_reader)

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_writer = OdtWriter(DocumentToOdtConverter(), xml_parser)

    markdown_to_odt_configuration: MarkdownToOdtConfiguration = serializer.deserialize_from_file(configuration_file_path, MarkdownToOdtConfiguration)
    document_content = load_document(markdown_reader, serializer, definition_file_path, source_file_path)

    odt_writer.write_as_single_document(
        output_file_path = destination_file_path,
        document_content = document_content,
        document_comments = [],
        template_file_path = markdown_to_odt_configuration.fodt_template_file_path,
        flat_odt = True,
        simulate = simulate)


def load_document(
        document_reader: DocumentReader, serializer: Serializer, definition_file_path: Optional[str], source_file_path: Optional[str]) -> RootElement:

    if definition_file_path is not None:
        document_definition: DocumentDefinition = serializer.deserialize_from_file(definition_file_path, DocumentDefinition)
        return document_operations.load_document_from_definition(document_definition, document_reader)

    if source_file_path is not None:
        return document_reader.read_content_from_file(source_file_path)

    raise ValueError("'definition_file_path' or 'source_file_path' must be set")


def convert_styles(serializer: Serializer, document_content: RootElement, style_map_file_path: str) -> None:
    style_map_configuration: dict = serializer.deserialize_from_file(style_map_file_path, dict)
    style_map = { style["markdown"]: style["odt"] for style in style_map_configuration["style_collection"] }

    document_operations.convert_styles(document_content, style_map)


if __name__ == "__main__":
    main()
