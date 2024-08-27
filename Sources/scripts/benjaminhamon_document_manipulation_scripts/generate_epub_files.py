import argparse
import os
import shutil

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.epub import epub_package_configuration_builder
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_document_manipulation_toolkit.epub.epub_generation_configuration import EpubGenerationConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_generation_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_content_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    generate_epub_files(
        serializer = create_serializer(os.path.splitext(arguments.configuration)[1].lstrip(".")),
        configuration_file_path = os.path.normpath(arguments.configuration),
        destination_directory = os.path.normpath(arguments.destination),
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description = "Generate files for an epub package.")
    argument_parser.add_argument("--configuration", required = True, metavar = "<path>", help = "path to the epub configuration")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the directory where to create the new files")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    serializer = serializer_factory.create_serializer(serialization_type)
    serializer.add_converter(EpubGenerationConfiguration, epub_generation_configuration_serialization_converter.factory())
    serializer.add_converter(EpubContentConfiguration, epub_content_configuration_serialization_converter.factory())
    return serializer


def generate_epub_files(
        serializer: Serializer,
        configuration_file_path: str,
        destination_directory: str,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if os.path.exists(destination_directory):
        if not overwrite:
            raise RuntimeError("Destination already exists")

    epub_generation_configuration: EpubGenerationConfiguration \
        = serializer.deserialize_from_file(configuration_file_path, EpubGenerationConfiguration)

    epub_generation_configuration.resolve_file_patterns()

    epub_package_configuration = epub_package_configuration_builder.create_package_configuration(epub_generation_configuration, destination_directory)

    epub_content_configuration_file_path = os.path.join(destination_directory, "content.yaml")
    container_file_path = os.path.join(destination_directory, "container.xml")
    package_document_file_path = os.path.join(destination_directory, "content.opf")
    package_document_file_path_in_archive = os.path.join("EPUB", "content.opf")
    toc_file_path = os.path.join(destination_directory, "toc.xhtml")

    content_writer = EpubContentWriter()

    if not simulate:
        if os.path.exists(destination_directory):
            shutil.rmtree(destination_directory)
        os.makedirs(destination_directory)

    content_writer.write_package_document_file(package_document_file_path, epub_package_configuration.document, "EPUB", simulate = simulate)
    content_writer.write_navigation_file(toc_file_path, epub_package_configuration.navigation, "EPUB", simulate = simulate)
    content_writer.write_container_file(container_file_path, package_document_file_path_in_archive, simulate = simulate)

    if not simulate:
        serializer.serialize_to_file(epub_package_configuration.content_configuration, epub_content_configuration_file_path)


if __name__ == "__main__":
    main()
