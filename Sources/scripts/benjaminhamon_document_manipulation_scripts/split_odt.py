# cspell:words fodt lxml

import argparse
import os
import shutil
from typing import Optional

import lxml.etree

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.open_document.document_to_odt_converter import DocumentToOdtConverter
from benjaminhamon_document_manipulation_toolkit.open_document.odt_reader import OdtReader
from benjaminhamon_document_manipulation_toolkit.open_document.odt_to_document_converter import OdtToDocumentConverter
from benjaminhamon_document_manipulation_toolkit.open_document.odt_writer import OdtWriter


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    split_odt(
        source_file_path = os.path.normpath(arguments.source),
        destination_directory = os.path.normpath(arguments.destination),
        template_file_path = os.path.normpath(arguments.template) if arguments.template is not None else None,
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description = "Split an odt file into one file per section.")
    argument_parser.add_argument("--source", required = True, metavar = "<path>", help = "path to the odt or fodt file to use as the source")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the directory where to create the new fodt files")
    argument_parser.add_argument("--template", metavar = "<path>", help = "path to the fodt file to use as the template")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the destination if it exists")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def split_odt(
        source_file_path: str,
        destination_directory: str,
        template_file_path: Optional[str] = None,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if os.path.exists(destination_directory):
        if not overwrite:
            raise RuntimeError("Destination already exists: '%s'" % destination_directory)

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(OdtToDocumentConverter(), xml_parser)
    odt_writer = OdtWriter(DocumentToOdtConverter(), xml_parser)

    document_content = odt_reader.read_content_from_file(source_file_path)
    document_comments = odt_reader.read_comments_from_file(source_file_path)

    if not simulate:
        if os.path.exists(destination_directory):
            shutil.rmtree(destination_directory)
        os.makedirs(destination_directory)

    odt_writer.write_as_many_documents(
        destination_directory, document_content, document_comments,
        template_file_path = template_file_path, flat_odt = True, simulate = simulate)


if __name__ == "__main__":
    main()
