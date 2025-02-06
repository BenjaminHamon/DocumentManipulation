import argparse
import datetime
import os
from typing import Mapping, Optional

import lxml.etree
import lxml.html

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_scripts.revision_control.git_client import GitClient
from benjaminhamon_document_manipulation_scripts.revision_control.revision_control_client import RevisionControlClient
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.documents.serialization import document_information_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_document_manipulation_toolkit.epub.document_to_xhtml_converter import DocumentToXhtmlConverter
from benjaminhamon_document_manipulation_toolkit.epub.epub_xhtml_writer import EpubXhtmlWriter
from benjaminhamon_document_manipulation_toolkit.html import html_operations
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata
from benjaminhamon_document_manipulation_toolkit.metadata.serialization import dc_metadata_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer
from benjaminhamon_document_manipulation_toolkit.xml import xml_operations


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    generate_information_as_xhtml(
        serializer = create_serializer(os.path.splitext(arguments.information)[1].lstrip(".")),
        information_file_path = os.path.normpath(arguments.information) if arguments.information is not None else None,
        dc_metadata_file_path = os.path.normpath(arguments.metadata) if arguments.metadata is not None else None,
        destination_file_path = os.path.normpath(arguments.destination),
        template_file_path = os.path.normpath(arguments.template),
        revision_control = arguments.revision_control,
        extra_information = dict(arguments.extra),
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:

    def parse_key_value_parameter(argument_value):
        key_value = argument_value.split("=")
        if len(key_value) != 2:
            raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
        return (key_value[0], key_value[1])

    argument_parser = argparse.ArgumentParser(description = "Generate document information as xhtml.")
    argument_parser.add_argument("--information", metavar = "<path>", help = "path to an information yaml file")
    argument_parser.add_argument("--metadata", metavar = "<path>", help = "path to a metadata yaml file")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the file to create")
    argument_parser.add_argument("--template", required = True, metavar = "<path>", help = "path to the xhtml file to use as the template")
    argument_parser.add_argument("--revision-control", metavar="<revision_control>", help = "retrieve information from revision control")
    argument_parser.add_argument("--extra", nargs = "*", type = parse_key_value_parameter, default = [],
        metavar = "<key=value>", help = "provide extra information as key value pairs")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the files if they exist")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    serializer = serializer_factory.create_serializer(serialization_type)
    serializer.add_converter(DcMetadata, dc_metadata_serialization_converter.factory())
    serializer.add_converter(DocumentInformation, document_information_serialization_converter.factory())
    return serializer


def generate_information_as_xhtml( # pylint: disable = too-many-arguments, too-many-locals
        serializer: Serializer,
        information_file_path: Optional[str],
        dc_metadata_file_path: Optional[str],
        destination_file_path: str,
        template_file_path: str,
        revision_control: Optional[str],
        extra_information: Mapping[str,str],
        now: Optional[datetime.datetime] = None,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)

    if os.path.exists(destination_file_path):
        if not overwrite:
            raise RuntimeError("Destination already exists: '%s'" % destination_file_path)

    document_metadata = script_helpers.gather_document_metadata(
        serializer = serializer,
        information_file_path = information_file_path,
        dc_metadata_file_path = dc_metadata_file_path,
        revision_control = revision_control,
        date = now,
        extra_metadata = extra_information)

    xhtml_parser = lxml.html.XHTMLParser(remove_blank_text = True)
    xhtml_writer = EpubXhtmlWriter(DocumentToXhtmlConverter(), xhtml_parser)

    xhtml_document = epub_xhtml_helpers.create_xhtml_base("Information", xhtml_parser, template_file_path)
    for link_element in epub_xhtml_helpers.try_find_xhtml_element_collection(xhtml_document.getroot(), "//x:link"):
        html_operations.update_link(link_element, template_file_path, destination_file_path)

    xml_operations.format_text_in_xml(xhtml_document.getroot(), document_metadata)
    xhtml_writer.write_to_file(destination_file_path, xhtml_document, simulate = simulate)


def create_revision_control_client(revision_control: str) -> RevisionControlClient:
    if revision_control == "git":
        return GitClient()

    raise ValueError("Unsupported revision control: '%s'" % revision_control)


if __name__ == "__main__":
    main()
