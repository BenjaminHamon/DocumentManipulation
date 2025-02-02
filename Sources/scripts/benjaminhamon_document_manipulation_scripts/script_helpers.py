# cspell:words levelname

import datetime
import logging
from typing import Dict, Mapping, Optional

from benjaminhamon_document_manipulation_scripts.revision_control.git_client import GitClient
from benjaminhamon_document_manipulation_scripts.revision_control.revision_control_client import RevisionControlClient
from benjaminhamon_document_manipulation_toolkit.documents import metadata_operations
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


all_logging_levels = [ "debug", "info", "warning", "error", "critical" ]


def get_logging_level_as_integer(level_as_string: str) -> int:
    if level_as_string.lower() == "debug":
        return logging.DEBUG
    if level_as_string.lower() == "info":
        return logging.INFO
    if level_as_string.lower() == "warning":
        return logging.WARNING
    if level_as_string.lower() == "error":
        return logging.ERROR
    if level_as_string.lower() == "critical":
        return logging.CRITICAL

    raise ValueError("Unknown logging level '%s'" % level_as_string)


def configure_logging(verbosity: str) -> None:
    logging.basicConfig(
        level = get_logging_level_as_integer(verbosity),
        format = "[{levelname}][{name}] {message}",
        datefmt = "%Y-%m-%dT%H:%M:%S",
        style = "{")


def gather_document_metadata( # pylint: disable = too-many-arguments
        serializer: Serializer,
        metadata_from_source: Optional[Mapping[str,str]] = None,
        information_file_path: Optional[str] = None,
        dc_metadata_file_path: Optional[str] = None,
        revision_control: Optional[str] = None,
        date: Optional[datetime.datetime] = None,
        extra_metadata: Optional[Mapping[str,str]] = None) -> Dict[str,str]:

    def create_revision_control_client(revision_control: str) -> RevisionControlClient:
        if revision_control == "git":
            return GitClient()

        raise ValueError("Unsupported revision control: '%s'" % revision_control)

    document_metadata: Dict[str,str] = {}

    if metadata_from_source is not None:
        document_metadata.update(metadata_from_source)

    if information_file_path is not None:
        document_information: DocumentInformation = serializer.deserialize_from_file(information_file_path, DocumentInformation)
        document_metadata.update(metadata_operations.convert_document_information_to_dict(document_information))

    if dc_metadata_file_path is not None:
        dc_metadata: DcMetadata = serializer.deserialize_from_file(dc_metadata_file_path, DcMetadata)
        document_metadata.update(metadata_operations.convert_dc_metadata_to_dict(dc_metadata))

    if revision_control is not None:
        revision_control_client = create_revision_control_client(revision_control)
        document_metadata.update(metadata_operations.get_revision_control_information(revision_control_client))

    if date is not None:
        document_metadata["date"] = date.strftime("%d-%b-%Y")

    if extra_metadata is not None:
        document_metadata.update(extra_metadata)

    return document_metadata
