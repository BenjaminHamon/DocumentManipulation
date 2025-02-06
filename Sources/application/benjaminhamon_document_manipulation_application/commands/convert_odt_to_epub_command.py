import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.convert_odt_to_epub import convert_odt_to_epub


logger = logging.getLogger("Main")


class ConvertOdtToEpubCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:

        def parse_key_value_parameter(argument_value):
            key_value = argument_value.split("=")
            if len(key_value) != 2:
                raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
            return (key_value[0], key_value[1])

        argument_parser = subparsers.add_parser("convert-odt-to-epub",
            help = "convert an odt file to an epub package")

        argument_parser.add_argument("--configuration", required = True,
            metavar = "<path>", help = "path to the conversion configuration")
        argument_parser.add_argument("--definition",
            metavar = "<path>", help = "path to the document definition (set this or source)")
        argument_parser.add_argument("--source",
            metavar = "<path>", help = "path to the source document (set this or definition)")
        argument_parser.add_argument("--destination", required = True,
            metavar = "<path>", help = "path to the epub package to create")
        argument_parser.add_argument("--intermediate", required = True,
            metavar = "<path>", help = "path to the directory where to create the intermediate files")
        argument_parser.add_argument("--extra", nargs = "*", type = parse_key_value_parameter, default = [],
            metavar = "<key=value>", help = "provide extra information as key value pairs")
        argument_parser.add_argument("--overwrite", action = "store_true",
            help = "overwrite the destination file or directory in case it already exists")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        convert_odt_to_epub(
            configuration_file_path = os.path.normpath(arguments.configuration),
            definition_file_path = os.path.normpath(arguments.definition) if arguments.definition is not None else None,
            source_file_path = os.path.normpath(arguments.source) if arguments.source is not None else None,
            destination_file_path = os.path.normpath(arguments.destination),
            intermediate_directory = os.path.normpath(arguments.intermediate),
            extra_information = dict(arguments.extra),
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
