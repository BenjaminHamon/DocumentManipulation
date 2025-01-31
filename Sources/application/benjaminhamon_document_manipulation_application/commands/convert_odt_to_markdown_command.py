import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.convert_odt_to_markdown import convert_odt_to_markdown

logger = logging.getLogger("Main")


class ConvertOdtToMarkdownCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        argument_parser = subparsers.add_parser("convert-odt-to-markdown",
            help = "convert an odt document to a markdown document")

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

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        convert_odt_to_markdown(
            configuration_file_path = os.path.normpath(arguments.configuration),
            definition_file_path = os.path.normpath(arguments.definition) if arguments.definition is not None else None,
            source_file_path = os.path.normpath(arguments.source) if arguments.source is not None else None,
            destination_file_path_or_directory = os.path.normpath(arguments.destination),
            write_as_single_file = arguments.single_file,
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
