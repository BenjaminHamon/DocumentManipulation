import argparse
import datetime
import os
import shutil
from typing import Dict, Optional

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_builder import EpubPackageBuilder
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_content_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    stage_files_for_epub_package(
        serializer = create_serializer(os.path.splitext(arguments.configuration)[1].lstrip(".")),
        configuration_file_path = os.path.normpath(arguments.configuration),
        destination_directory = os.path.normpath(arguments.destination),
        parameters = dict(arguments.parameters),
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:

    def parse_key_value_parameter(argument_value):
        key_value = argument_value.split("=")
        if len(key_value) != 2:
            raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
        return (key_value[0], key_value[1])

    argument_parser = argparse.ArgumentParser(description = "Generate files for an EPUB package")
    argument_parser.add_argument("--configuration", required = True, metavar = "<path>", help = "path to the epub content configuration")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the directory where to create the new files")
    argument_parser.add_argument("--parameters", nargs = "*", type = parse_key_value_parameter, default = [],
        metavar = "<key=value>", help = "parameters for the files")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    serializer = serializer_factory.create_serializer(serialization_type)
    serializer.add_converter(EpubContentConfiguration, epub_content_configuration_serialization_converter.factory())
    return serializer


def stage_files_for_epub_package( # pylint: disable = too-many-arguments
        serializer: Serializer,
        configuration_file_path: str,
        destination_directory: str,
        parameters: Dict[str,str],
        modified: Optional[datetime.datetime] = None,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if modified is None:
        modified = datetime.datetime.now(datetime.timezone.utc)

    if os.path.exists(destination_directory):
        if not overwrite:
            raise RuntimeError("Destination already exists")

    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    epub_content_configuration: EpubContentConfiguration = serializer.deserialize_from_file(configuration_file_path, EpubContentConfiguration)
    parameters["modified"] = modified.astimezone(datetime.timezone.utc).replace(tzinfo = None).isoformat() + "Z"

    if not simulate:
        if os.path.exists(destination_directory):
            shutil.rmtree(destination_directory)
        os.makedirs(destination_directory)

    package_builder.stage_files(destination_directory, epub_content_configuration.file_mappings, simulate = simulate)

    if not simulate:
        package_builder.update_xhtml_links(
            destination_directory, epub_content_configuration.file_mappings, epub_content_configuration.link_mappings, simulate = simulate)
        package_builder.update_package_information(os.path.join(destination_directory, "EPUB", "content.opf"), parameters, simulate = simulate)


if __name__ == "__main__":
    main()
