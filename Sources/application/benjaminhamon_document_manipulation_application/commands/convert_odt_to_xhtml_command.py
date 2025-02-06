# cspell:words fodt

import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.convert_odt_to_xhtml import convert_odt_to_xhtml


logger = logging.getLogger("Main")


class ConvertOdtToXhtmlCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        argument_parser = subparsers.add_parser("convert-odt-to-xhtml", help = "convert odt files to xhtml")
        argument_parser.add_argument("--source", required = True, nargs = "+", metavar = "<path>", help = "paths to the odt or fodt files to use as the source")
        argument_parser.add_argument("--output", required = True, metavar = "<path>", help = "path to the directory where to create the new xhtml files")
        argument_parser.add_argument("--template", metavar = "<path>", help = "path to the xhtml file to use as the template")
        argument_parser.add_argument("--style-sheet", metavar = "<path>", help = "path to the css file for the new xhtml files")
        argument_parser.add_argument("--style-map", metavar = "<path>", help = "path to the yaml file for a style conversion map")
        argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the destination if it exists")
        argument_parser.add_argument("--section-regex", metavar = "<regex>", help = "filter the content based on section title")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        convert_odt_to_xhtml(
            source_file_path_collection = [ os.path.normpath(path) for path in arguments.source ],
            destination_directory = os.path.normpath(arguments.output),
            template_file_path = os.path.normpath(arguments.template) if arguments.template is not None else None,
            style_sheet_file_path = os.path.normpath(arguments.style_sheet) if arguments.template is not None else None,
            style_map_file_path = arguments.style_map,
            section_regex = arguments.section_regex,
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
