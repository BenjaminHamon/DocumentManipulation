from typing import Dict
from benjaminhamon_document_manipulation_scripts.revision_control.revision_control_client import RevisionControlClient
from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata


def convert_document_information_to_dict(document_information: DocumentInformation) -> Dict[str,str]:
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


def convert_dc_metadata_to_dict(dc_metadata: DcMetadata) -> Dict[str,str]:
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


def get_revision_control_information(revision_control_client: RevisionControlClient) -> Dict[str,str]:
    data = {}

    branch = revision_control_client.get_current_branch()
    if branch is not None:
        data["branch"] = branch

    data["revision"] = revision_control_client.get_current_revision()
    data["revision_short"] = revision_control_client.convert_revision_to_short(data["revision"])
    data["revision_date"] = revision_control_client.get_revision_date(data["revision"]).replace(tzinfo = None).isoformat() + "Z"

    return data
