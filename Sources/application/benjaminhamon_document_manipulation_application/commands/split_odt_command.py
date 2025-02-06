# cspell:words fodt

import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.split_odt import split_odt


logger = logging.getLogger("Main")


class SplitOdtCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        argument_parser = subparsers.add_parser("split-odt", help = "split an odt file into one file per section")
        argument_parser.add_argument("--source", required = True, metavar = "<path>", help = "path to the odt or fodt file to use as the source")
        argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the directory where to create the new fodt files")
        argument_parser.add_argument("--template", metavar = "<path>", help = "path to the fodt file to use as the template")
        argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the destination if it exists")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        split_odt(
            source_file_path = os.path.normpath(arguments.source),
            destination_directory = os.path.normpath(arguments.destination),
            template_file_path = os.path.normpath(arguments.template) if arguments.template is not None else None,
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
