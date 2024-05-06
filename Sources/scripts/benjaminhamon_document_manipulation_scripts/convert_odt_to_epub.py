# cspell:words fodt

import argparse
import datetime
import glob
import os
import shutil
import tempfile
from typing import List, Mapping, Optional

from benjaminhamon_document_manipulation_scripts import script_helpers
from benjaminhamon_document_manipulation_scripts.convert_odt_to_xhtml import convert_odt_to_xhtml
from benjaminhamon_document_manipulation_scripts.create_epub_package import create_epub_package
from benjaminhamon_document_manipulation_scripts.generate_epub_files import generate_epub_files
from benjaminhamon_document_manipulation_scripts.generate_information_as_xhtml import generate_information_as_xhtml
from benjaminhamon_document_manipulation_scripts.rewrite_odt import rewrite_odt
from benjaminhamon_document_manipulation_scripts.stage_files_for_epub_package import stage_files_for_epub_package
from benjaminhamon_document_manipulation_toolkit.conversion.odt_to_epub_configuration import OdtToEpubConfiguration
from benjaminhamon_document_manipulation_toolkit.conversion.serialization import odt_to_epub_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.documents.serialization import document_information_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub import epub_metadata_builder
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_generation_configuration import EpubGenerationConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_content_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_generation_configuration_serialization_converter
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata
from benjaminhamon_document_manipulation_toolkit.metadata.serialization import dc_metadata_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization import serializer_factory
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


def main() -> None:
    arguments = parse_arguments()

    script_helpers.configure_logging(arguments.verbosity)

    convert_odt_to_epub(
        serializer = create_serializer(os.path.splitext(arguments.configuration)[1].lstrip(".")),
        configuration_file_path = os.path.normpath(arguments.configuration),
        destination_file_path = os.path.normpath(arguments.destination),
        intermediate_directory = os.path.normpath(arguments.intermediate) if arguments.intermediate is not None else None,
        extra_information = dict(arguments.extra),
        overwrite = arguments.overwrite)


def parse_arguments() -> argparse.Namespace:

    def parse_key_value_parameter(argument_value):
        key_value = argument_value.split("=")
        if len(key_value) != 2:
            raise argparse.ArgumentTypeError("invalid key value parameter: '%s'" % argument_value)
        return (key_value[0], key_value[1])

    argument_parser = argparse.ArgumentParser(description = "Generate files for an EPUB package")
    argument_parser.add_argument("--configuration", required = True, metavar = "<path>", help = "path to the epub configuration")
    argument_parser.add_argument("--destination", required = True, metavar = "<path>", help = "path to the epub package to create")
    argument_parser.add_argument("--intermediate", metavar = "<path>", help = "path to the directory where to create the intermediate files")
    argument_parser.add_argument("--extra", nargs = "*", type = parse_key_value_parameter, default = [],
        metavar = "<key=value>", help = "provide extra information as key value pairs")
    argument_parser.add_argument("--overwrite", action = "store_true", help = "overwrite the destination file in case it already exists")

    argument_parser.add_argument("--verbosity", choices = script_helpers.all_logging_levels, default = "info", type = str.lower,
        metavar = "<level>", help = "set the logging level (%s)" % ", ".join(script_helpers.all_logging_levels))

    arguments = argument_parser.parse_args()

    return arguments


def create_serializer(serialization_type: str) -> Serializer:
    serializer = serializer_factory.create_serializer(serialization_type)
    serializer.add_converter(DcMetadata, dc_metadata_serialization_converter.factory())
    serializer.add_converter(DocumentInformation, document_information_serialization_converter.factory())
    serializer.add_converter(EpubContentConfiguration, epub_content_configuration_serialization_converter.factory())
    serializer.add_converter(EpubGenerationConfiguration, epub_generation_configuration_serialization_converter.factory())
    serializer.add_converter(OdtToEpubConfiguration, odt_to_epub_configuration_serialization_converter.factory())
    return serializer


def convert_odt_to_epub( # pylint: disable = too-many-arguments, too-many-locals
        serializer: Serializer,
        configuration_file_path: str,
        destination_file_path: str,
        intermediate_directory: Optional[str],
        extra_information: Mapping[str,str],
        now: Optional[datetime.datetime] = None,
        overwrite: bool = False,
        simulate: bool = False) -> None:

    if simulate:
        raise NotImplementedError("Simulate option is not supported")

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)

    if os.path.exists(destination_file_path):
        if not overwrite:
            raise RuntimeError("Destination already exists")

    odt_to_epub_configuration = serializer.deserialize_from_file(configuration_file_path, OdtToEpubConfiguration)
    if odt_to_epub_configuration.source_file_path is None:
        raise ValueError("source_file_path is required")

    metadata_items = load_metadata(serializer, odt_to_epub_configuration)

    if intermediate_directory is not None:
        if not simulate:
            if os.path.exists(intermediate_directory):
                shutil.rmtree(intermediate_directory)
            os.makedirs(intermediate_directory)

    if intermediate_directory is None:
        intermediate_directory = tempfile.mkdtemp()

    intermediate_fodt_file_path = os.path.join(intermediate_directory, "FullText.fodt")
    intermediate_xhtml_extra_directory = os.path.join(intermediate_directory, "ExtraAsXhtml")
    intermediate_xhtml_section_directory = os.path.join(intermediate_directory, "SectionsAsXhtml")
    intermediate_epub_generation_file_path = os.path.join(intermediate_directory, "EpubGenerationConfiguration.yaml")
    intermediate_epub_file_directory = os.path.join(intermediate_directory, "EpubFiles")
    intermediate_staging_directory = os.path.join(intermediate_directory, "Staging")

    rewrite_odt(
        source_file_path = odt_to_epub_configuration.source_file_path,
        destination_file_path = intermediate_fodt_file_path,
        template_file_path = odt_to_epub_configuration.fodt_template_file_path,
        simulate = simulate)

    if not simulate:
        os.makedirs(intermediate_xhtml_extra_directory)

    if odt_to_epub_configuration.xhtml_information_template_file_path is not None:
        generate_information_as_xhtml(
            serializer = serializer,
            information_file_path = odt_to_epub_configuration.information_file_path,
            dc_metadata_file_path = odt_to_epub_configuration.dc_metadata_file_path,
            destination_file_path = os.path.join(intermediate_xhtml_extra_directory, "Information.xhtml"),
            template_file_path = odt_to_epub_configuration.xhtml_information_template_file_path,
            revision_control = odt_to_epub_configuration.revision_control,
            extra_information = extra_information,
            now = now,
            simulate = simulate)

    convert_odt_to_xhtml(
        source_file_path_collection = [ intermediate_fodt_file_path ],
        destination_directory = intermediate_xhtml_section_directory,
        template_file_path = odt_to_epub_configuration.xhtml_section_template_file_path,
        style_sheet_file_path = odt_to_epub_configuration.style_sheet_file_path,
        section_regex = odt_to_epub_configuration.source_section_regex,
        simulate = simulate)

    write_epub_generation_configuration(
        serializer = serializer,
        configuration_file_path = intermediate_epub_generation_file_path,
        metadata = metadata_items,
        odt_to_epub_configuration = odt_to_epub_configuration,
        xhtml_directory = intermediate_xhtml_section_directory,
        simulate = simulate)

    generate_epub_files(
        serializer = serializer,
        configuration_file_path = intermediate_epub_generation_file_path,
        destination_directory = intermediate_epub_file_directory,
        simulate = simulate)

    stage_files_for_epub_package(
        serializer = serializer,
        configuration_file_path = os.path.join(intermediate_epub_file_directory, "content.yaml"),
        destination_directory = intermediate_staging_directory,
        parameters = {},
        modified = now,
        simulate = simulate)

    create_epub_package(
        source_directory = intermediate_staging_directory,
        destination_file_path = destination_file_path,
        overwrite = overwrite,
        simulate = simulate)


def load_metadata(serializer: Serializer, odt_to_epub_configuration: OdtToEpubConfiguration) -> List[EpubMetadataItem]:
    if odt_to_epub_configuration.dc_metadata_file_path is not None:
        dc_metadata: DcMetadata = serializer.deserialize_from_file(odt_to_epub_configuration.dc_metadata_file_path, DcMetadata)
        return epub_metadata_builder.create_epub_metadata_from_dc_metadata(dc_metadata)

    if odt_to_epub_configuration.information_file_path is not None:
        document_information: DocumentInformation = serializer.deserialize_from_file(odt_to_epub_configuration.information_file_path, DocumentInformation)
        return epub_metadata_builder.create_epub_metadata_from_document_information(document_information)

    return []


def write_epub_generation_configuration( # pylint: disable = too-many-arguments
        serializer: Serializer,
        configuration_file_path: str,
        metadata: List[EpubMetadataItem],
        odt_to_epub_configuration: OdtToEpubConfiguration,
        xhtml_directory: str,
        simulate: bool = False) -> None:

    epub_generation_configuration = EpubGenerationConfiguration()
    epub_generation_configuration.metadata = metadata
    epub_generation_configuration.cover_file = odt_to_epub_configuration.cover_file

    epub_generation_configuration.content_files = []
    epub_generation_configuration.content_files += odt_to_epub_configuration.content_files_before
    epub_generation_configuration.content_files += glob.glob(os.path.join(xhtml_directory, "*.xhtml"))
    epub_generation_configuration.content_files += odt_to_epub_configuration.content_files_after

    epub_generation_configuration.resource_files = odt_to_epub_configuration.resource_files
    epub_generation_configuration.link_overrides = odt_to_epub_configuration.link_overrides
    epub_generation_configuration.landmarks = odt_to_epub_configuration.landmarks

    if not simulate:
        serializer.serialize_to_file(epub_generation_configuration, configuration_file_path)


if __name__ == "__main__":
    main()
