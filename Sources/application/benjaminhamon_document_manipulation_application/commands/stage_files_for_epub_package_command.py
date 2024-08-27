import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.stage_files_for_epub_package import create_serializer, stage_files_for_epub_package


logger = logging.getLogger("Main")


class StageFilesForEpubPackageCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:

        def parse_key_value_parameter(argument_value):
            key_value = argument_value.split("=")
            if len(key_value) != 2:
                raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
            return (key_value[0], key_value[1])

        argument_parser = subparsers.add_parser("stage-files-for-epub-package", help = "stage files for creating an epub package")
        argument_parser.add_argument("--configuration", required = True, metavar = "<path>", help = "path to the epub content configuration")
        argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the directory where to create the new files")
        argument_parser.add_argument("--parameters", nargs = "*", type = parse_key_value_parameter, default = [],
            metavar = "<key=value>", help = "parameters for the files")
        argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        stage_files_for_epub_package(
            serializer = create_serializer(os.path.splitext(arguments.configuration)[1].lstrip(".")),
            configuration_file_path = os.path.normpath(arguments.configuration),
            destination_directory = os.path.normpath(arguments.destination),
            parameters = dict(arguments.parameters),
            overwrite = arguments.overwrite)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
