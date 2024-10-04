import argparse
import datetime
import os
from typing import Mapping, Optional

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_scripts.revision_control.git_client import GitClient
from benjaminhamon_document_manipulation_scripts.revision_control.revision_control_client import RevisionControlClient
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.documents.serialization import document_information_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_xhtml_builder import EpubContentXhtmlBuilder
from benjaminhamon_document_manipulation_toolkit.epub.epub_xhtml_writer import EpubXhtmlWriter
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
            raise RuntimeError("Destination already exists")

    format_parameters: Mapping[str,str] = {}

    if information_file_path is not None:
        format_parameters.update(get_parameters_from_document_information(serializer, information_file_path))

    if dc_metadata_file_path is not None:
        format_parameters.update(get_parameters_from_dc_metadata(serializer, dc_metadata_file_path))

    if revision_control is not None:
        revision_control_client = create_revision_control_client(revision_control)
        format_parameters.update(get_parameters_from_revision_control(revision_control_client))

    format_parameters["date"] = now.strftime("%d-%b-%Y")
    format_parameters.update(extra_information)

    xhtml_writer = EpubXhtmlWriter()
    xhtml_builder = EpubContentXhtmlBuilder("Information", template_file_path)
    xhtml_builder.update_links(template_file_path, destination_file_path)
    xhtml_document = xhtml_builder.get_xhtml_document()
    xml_operations.format_text_in_xml(xhtml_document.getroot(), format_parameters)
    xhtml_writer.write_to_file(destination_file_path, xhtml_document, simulate = simulate)


def get_parameters_from_document_information(serializer: Serializer, information_file_path: str) -> dict:
    document_information: DocumentInformation = serializer.deserialize_from_file(information_file_path, DocumentInformation)

    data = {}
    if document_information.identifier is not None:
        data["identifier"] = document_information.identifier
    if document_information.language is not None:
        data["language"] = document_information.language
    if document_information.title is not None:
        data["title"] = document_information.title
    if document_information.author is not None:
        data["author"] = document_information.author
    if document_information.publisher is not None:
        data["publisher"] = document_information.publisher
    if document_information.publication_date is not None:
        data["publication_date"] = document_information.publication_date.strftime("%d-%b-%Y")
    if document_information.copyright is not None:
        data["copyright"] = document_information.copyright
    if document_information.version_identifier is not None:
        data["version_identifier"] = document_information.version_identifier
    if document_information.version_display_name is not None:
        data["version_display_name"] = document_information.version_display_name

    return data


def get_parameters_from_dc_metadata(serializer: Serializer, dc_metadata_file_path: str) -> dict:
    dc_metadata: DcMetadata = serializer.deserialize_from_file(dc_metadata_file_path, DcMetadata)

    data = {}
    if dc_metadata.identifiers is not None and len(dc_metadata.identifiers) > 0:
        data["identifier"] = dc_metadata.identifiers[0]
    if dc_metadata.languages is not None and len(dc_metadata.languages) > 0:
        data["language"] = dc_metadata.languages[0]
    if dc_metadata.titles is not None and len(dc_metadata.titles) > 0:
        data["title"] = dc_metadata.titles[0]
    if dc_metadata.creators is not None and len(dc_metadata.creators) > 0:
        data["author"] = dc_metadata.creators[0].name
    if dc_metadata.publishers is not None and len(dc_metadata.publishers) > 0:
        data["publisher"] = dc_metadata.publishers[0]
    if dc_metadata.dates is not None and len(dc_metadata.dates) > 0:
        data["publication_date"] = dc_metadata.dates[0]
    if dc_metadata.rights is not None and len(dc_metadata.rights) > 0:
        data["copyright"] = dc_metadata.rights[0]

    return data


def get_parameters_from_revision_control(revision_control_client: RevisionControlClient) -> dict:
    data = {}

    branch = revision_control_client.get_current_branch()
    if branch is not None:
        data["branch"] = branch

    data["revision"] = revision_control_client.get_current_revision()
    data["revision_short"] = revision_control_client.convert_revision_to_short(data["revision"])
    data["revision_date"] = revision_control_client.get_revision_date(data["revision"]).replace(tzinfo = None).isoformat() + "Z"

    return data


def create_revision_control_client(revision_control: str) -> RevisionControlClient:
    if revision_control == "git":
        return GitClient()

    raise ValueError("Unsupported revision control: '%s'" % revision_control)


if __name__ == "__main__":
    main()
