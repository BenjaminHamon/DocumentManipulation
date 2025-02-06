import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.create_epub_package import create_epub_package


logger = logging.getLogger("Main")


class CreateEpubPackageCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        argument_parser = subparsers.add_parser("create-epub-package", help = "create an epub package")
        argument_parser.add_argument("--source", required = True, metavar = "<path>", help = "path to the epub source files")
        argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the epub package to create")
        argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        create_epub_package(
            source_directory = os.path.normpath(arguments.source),
            destination_file_path = os.path.normpath(arguments.destination),
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
