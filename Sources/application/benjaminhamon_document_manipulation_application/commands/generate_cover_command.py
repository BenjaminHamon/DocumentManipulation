import argparse
import logging
import os

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_scripts.generate_cover import create_serializer, generate_cover


logger = logging.getLogger("Main")


class GenerateCoverCommand(ApplicationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:

        def parse_key_value_parameter(argument_value):
            key_value = argument_value.split("=")
            if len(key_value) != 2:
                raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
            return (key_value[0], key_value[1])

        argument_parser = subparsers.add_parser("generate-cover",
            help = "generate a document cover as svg.")
        argument_parser.add_argument("--information",
            metavar = "<path>", help = "path to an information yaml file")
        argument_parser.add_argument("--metadata",
            metavar = "<path>", help = "path to a metadata yaml file")
        argument_parser.add_argument("--destination", required = True,
            metavar = "<path>", help = "path to the file to create")
        argument_parser.add_argument("--template", required = True,
            metavar = "<path>", help = "path to the xhtml file to use as the template")
        argument_parser.add_argument("--format", required = True,
            metavar = "<image-format>", help = "set the format for the image to generate")
        argument_parser.add_argument("--revision-control",
            metavar="<revision_control>", help = "retrieve information from revision control")
        argument_parser.add_argument("--extra", nargs = "*", type = parse_key_value_parameter, default = [],
            metavar = "<key=value>", help = "provide extra information as key value pairs")
        argument_parser.add_argument("--overwrite", action = "store_true",
            help = "overwrite the files if they exist")

        return argument_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        generate_cover(
            serializer = create_serializer(os.path.splitext(arguments.information)[1].lstrip(".")),
            information_file_path = os.path.normpath(arguments.information) if arguments.information is not None else None,
            dc_metadata_file_path = os.path.normpath(arguments.metadata) if arguments.metadata is not None else None,
            destination_file_path = os.path.normpath(arguments.destination),
            template_file_path = os.path.normpath(arguments.template),
            image_format = arguments.format,
            revision_control = arguments.revision_control,
            extra_information = dict(arguments.extra),
            overwrite = arguments.overwrite,
            simulate = simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
