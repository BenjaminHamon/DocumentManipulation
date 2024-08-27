# cspell:words fodt lxml

import argparse
import os
from typing import Optional

import lxml.etree

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.open_document.odt_reader import OdtReader
from benjaminhamon_document_manipulation_toolkit.open_document.odt_writer import OdtWriter


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    rewrite_odt(
        source_file_path = os.path.normpath(arguments.source),
        destination_file_path = os.path.normpath(arguments.destination),
        template_file_path = os.path.normpath(arguments.template) if arguments.template is not None else None,
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description = "Rewrite an odt file into a lean and clean fodt file.")
    argument_parser.add_argument("--source", required = True, metavar = "<path>", help = "path to the odt or fodt source file")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the fodt file to write")
    argument_parser.add_argument("--template", metavar = "<path>", help = "path to the fodt file to use as the template")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the destination if it exists")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def rewrite_odt(
        source_file_path: str,
        destination_file_path: str,
        template_file_path: Optional[str] = None,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if os.path.exists(destination_file_path):
        if not overwrite:
            raise RuntimeError("Destination already exists")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_reader = OdtReader(xml_parser)
    odt_writer = OdtWriter(xml_parser)

    odt_content = odt_reader.read_fodt(source_file_path)
    document_content = odt_reader.read_content(odt_content)
    document_comments = odt_reader.read_comments(odt_content)

    odt_writer.write_as_single_document(
        destination_file_path, document_content, document_comments,
        template_file_path = template_file_path, flat_odt = True, simulate = simulate)


if __name__ == "__main__":
    main()
