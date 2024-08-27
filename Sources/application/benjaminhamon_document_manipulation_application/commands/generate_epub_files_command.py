import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.generate_epub_files import create_serializer, generate_epub_files


logger = logging.getLogger("Main")


class GenerateEpubFilesCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        argument_parser = subparsers.add_parser("generate-epub-files", help = "generate files for an epub package")
        argument_parser.add_argument("--configuration", required = True, metavar = "<path>", help = "path to the epub configuration")
        argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the directory where to create the new files")
        argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        generate_epub_files(
            serializer = create_serializer(os.path.splitext(arguments.configuration)[1].lstrip(".")),
            configuration_file_path = os.path.normpath(arguments.configuration),
            destination_directory = os.path.normpath(arguments.destination),
            overwrite = arguments.overwrite)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
