import argparse
import os
import shutil
from typing import Optional

import lxml.etree

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.conversion.odt_to_markdown_configuration import OdtToMarkdownConfiguration
from benjaminhamon_document_manipulation_toolkit.conversion.serialization import odt_to_markdown_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.documents.document_definition import DocumentDefinition
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.serialization import document_definition_serialization_converter
from benjaminhamon_document_manipulation_toolkit.documents.serialization import document_information_serialization_converter
from benjaminhamon_document_manipulation_toolkit.markdown.document_to_markdown_converter import DocumentToMarkdownConverter
from benjaminhamon_document_manipulation_toolkit.markdown.markdown_writer import MarkdownWriter
from benjaminhamon_document_manipulation_toolkit.open_document.odt_reader import OdtReader
from benjaminhamon_document_manipulation_toolkit.open_document.odt_to_document_converter import OdtToDocumentConverter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer
from benjaminhamon_document_manipulation_toolkit.serialization.yaml_serializer import YamlSerializer


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    convert_odt_to_markdown(
        configuration_file_path = os.path.normpath(arguments.configuration),
        definition_file_path = os.path.normpath(arguments.definition) if arguments.definition is not None else None,
        source_file_path = os.path.normpath(arguments.source) if arguments.source is not None else None,
        destination_file_path_or_directory = os.path.normpath(arguments.destination),
        write_as_single_file = arguments.single_file,
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(
        description = "Convert an odt document to a markdown document.")
    argument_parser.add_argument("--configuration", required = True,
        metavar = "<path>", help = "path to the conversion configuration")
    argument_parser.add_argument("--definition",
        metavar = "<path>", help = "path to the document definition (set this or source)")
    argument_parser.add_argument("--source",
        metavar = "<path>", help = "path to the source document (set this or definition)")
    argument_parser.add_argument("--destination", required = True,
        metavar = "<path>", help = "path to the document or directory to create")
    argument_parser.add_argument("--single-file", action = "store_true",
        help = "write the document as a single file")
    argument_parser.add_argument("--overwrite", action = "store_true",
        help = "overwrite the destination file or directory in case it already exists")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    serializer = serializer_factory.create_serializer(serialization_type)
    serializer.add_converter(DocumentDefinition, document_definition_serialization_converter.factory())
    serializer.add_converter(DocumentInformation, document_information_serialization_converter.factory())
    serializer.add_converter(OdtToMarkdownConfiguration, odt_to_markdown_configuration_serialization_converter.factory())
    return serializer


def convert_odt_to_markdown( # pylint: disable = too-many-arguments, too-many-locals
        configuration_file_path: str,
        definition_file_path: Optional[str],
        source_file_path: Optional[str],
        destination_file_path_or_directory: str,
        write_as_single_file: bool,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if definition_file_path is None and source_file_path is None:
        raise ValueError("Exactly one of 'definition_file_path' and 'source_file_path' must be set")
    if definition_file_path is not None and source_file_path is not None:
        raise ValueError("Exactly one of 'definition_file_path' and 'source_file_path' must be set")

    if os.path.exists(destination_file_path_or_directory):
        if not overwrite:
            raise RuntimeError("Destination already exists: '%s'" % destination_file_path_or_directory)

    serializer = create_serializer(os.path.splitext(configuration_file_path)[1].lstrip("."))
    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(OdtToDocumentConverter(), xml_parser)
    markdown_writer = MarkdownWriter(DocumentToMarkdownConverter(), YamlSerializer())

    odt_to_markdown_configuration: OdtToMarkdownConfiguration = serializer.deserialize_from_file(configuration_file_path, OdtToMarkdownConfiguration)
    document_definition: DocumentDefinition = script_helpers.load_document_definition(serializer, definition_file_path, source_file_path)

    extra_metadata: dict = {}
    if document_definition.extra_metadata is not None:
        extra_metadata.update(document_definition.extra_metadata)
    if odt_to_markdown_configuration.extra_metadata is not None:
        extra_metadata.update(odt_to_markdown_configuration.extra_metadata)

    document_metadata = script_helpers.gather_document_metadata(
        serializer = serializer,
        information_file_path = document_definition.information_file_path,
        dc_metadata_file_path = document_definition.dc_metadata_file_path,
        extra_metadata = extra_metadata,
        revision_control = odt_to_markdown_configuration.revision_control)

    document_content = document_operations.load_document_from_definition(document_definition, odt_reader)

    if odt_to_markdown_configuration.style_map_file_path is not None:
        convert_styles(serializer, document_content, odt_to_markdown_configuration.style_map_file_path)

    if write_as_single_file:
        markdown_writer.write_as_single_document(
            output_file_path = destination_file_path_or_directory,
            title = document_metadata["title"],
            metadata = document_metadata,
            content = document_content,
            simulate = simulate)

    else:
        if not simulate:
            if os.path.exists(destination_file_path_or_directory):
                shutil.rmtree(destination_file_path_or_directory)
            os.makedirs(destination_file_path_or_directory)

        markdown_writer.write_as_many_documents(
            output_directory = destination_file_path_or_directory,
            metadata = document_metadata,
            content = document_content,
            simulate = simulate)


def convert_styles(serializer: Serializer, document_content: RootElement, style_map_file_path: str) -> None:
    style_map_configuration: dict = serializer.deserialize_from_file(style_map_file_path, dict)
    style_map = { style["odt"]: style.get("markdown", None) for style in style_map_configuration["style_collection"] }

    document_operations.convert_styles(document_content, style_map)


if __name__ == "__main__":
    main()
