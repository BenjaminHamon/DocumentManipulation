import argparse
import os

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_builder import EpubPackageBuilder


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    create_epub_package(
        source_directory = os.path.normpath(arguments.source),
        destination_file_path = os.path.normpath(arguments.destination),
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:
    argument_parser = argparse.ArgumentParser(description = "Create an epub package.")
    argument_parser.add_argument("--source", required = True, metavar = "<path>", help = "path to the epub source files")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the epub package to create")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_epub_package(
        source_directory: str,
        destination_file_path: str,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if os.path.exists(destination_file_path):
        if not overwrite:
            raise RuntimeError("Destination already exists: '%s'" % destination_file_path)

    content_writer = EpubContentWriter()
    package_builder = EpubPackageBuilder(content_writer)

    package_builder.create_package(destination_file_path, source_directory, simulate = simulate)


if __name__ == "__main__":
    main()
