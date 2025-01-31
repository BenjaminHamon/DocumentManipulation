import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.convert_markdown_to_odt import convert_markdown_to_odt
from benjaminhamon_document_manipulation_scripts.convert_markdown_to_odt import create_serializer

logger = logging.getLogger("Main")


class ConvertMarkdownToOdtCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        argument_parser = subparsers.add_parser("convert-markdown-to-odt",
            help = "convert a markdown document to an odt document")

        argument_parser.add_argument("--configuration", required = True,
            metavar = "<path>", help = "path to the conversion configuration")
        argument_parser.add_argument("--definition",
            metavar = "<path>", help = "path to the document definition (set this or source)")
        argument_parser.add_argument("--source",
            metavar = "<path>", help = "path to the markdown document (set this or definition)")
        argument_parser.add_argument("--destination", required = True,
            metavar = "<path>", help = "path to the odt document to create")
        argument_parser.add_argument("--overwrite", action = "store_true",
            help = "overwrite the destination file in case it already exists")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
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
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
