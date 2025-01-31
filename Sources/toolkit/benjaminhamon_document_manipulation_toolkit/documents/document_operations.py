import fnmatch
import os
from typing import Dict, Iterator, List, Optional

from benjaminhamon_document_manipulation_toolkit import convert_helpers
from benjaminhamon_document_manipulation_toolkit.documents.document_definition import DocumentDefinition
from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.interfaces.document_reader import DocumentReader


def load_document_from_definition(document_definition: DocumentDefinition, document_reader: DocumentReader) -> RootElement:
    if document_definition.source_file_path is not None:
        return load_document_from_definition_as_single_file(document_definition, document_reader)

    if document_definition.source_directory is not None:
        return load_document_from_definition_as_many_files(document_definition, document_reader)

    raise ValueError("'source_file_path' or 'source_directory' must be set")


def load_document_from_definition_as_single_file(document_definition: DocumentDefinition, document_reader: DocumentReader) -> RootElement:

    def enumerate_matching_sections(section_identifier_collection: List[str]) -> Iterator[SectionElement]:
        for section in document_source.enumerate_sections():
            for section_identifier in section_identifier_collection:
                if fnmatch.fnmatch(section.get_heading().get_title(), section_identifier):
                    yield section

    if document_definition.source_file_path is None:
        raise ValueError("'source_file_path' must be set")

    document_source = document_reader.read_content_from_file(document_definition.source_file_path)

    document_content = RootElement()

    if document_definition.front_section_identifiers is not None:
        for section in enumerate_matching_sections(document_definition.front_section_identifiers):
            document_content.children.append(section)

    if document_definition.content_section_identifiers is not None:
        for section in enumerate_matching_sections(document_definition.content_section_identifiers):
            document_content.children.append(section)

    if document_definition.back_section_identifiers is not None:
        for section in enumerate_matching_sections(document_definition.back_section_identifiers):
            document_content.children.append(section)

    return document_content


def load_document_from_definition_as_many_files(document_definition: DocumentDefinition, document_reader: DocumentReader) -> RootElement:

    def read_section(section_file_path: str) -> RootElement:
        if document_definition.source_directory is not None:
            section_file_path = os.path.join(document_definition.source_directory, section_file_path)
        return document_reader.read_content_from_file(section_file_path)

    document_content = RootElement()

    if document_definition.front_section_file_paths is not None:
        for section_file_path in document_definition.front_section_file_paths:
            document_content.children.extend(read_section(section_file_path).children)

    if document_definition.content_section_file_paths is not None:
        for section_file_path in document_definition.content_section_file_paths:
            document_content.children.extend(read_section(section_file_path).children)

    if document_definition.back_section_file_paths is not None:
        for section_file_path in document_definition.back_section_file_paths:
            document_content.children.extend(read_section(section_file_path).children)

    return document_content


def enumerate_all_elements(element: DocumentElement) -> Iterator[DocumentElement]:
    yield element

    for child in element.children:
        yield from enumerate_all_elements(child)


def generate_section_file_name(section_title: str, section_index: int, section_count: int) -> str:
    title = str(section_index + 1).rjust(len(str(section_count)), "0") + " - " + section_title
    return convert_helpers.sanitize_for_file_name(title)


def convert_styles(root: DocumentElement, style_map: Dict[str,Optional[str]]) -> None:
    for element in enumerate_all_elements(root):
        new_style_collection = []
        for style in element.style_collection:
            if style not in style_map:
                raise ValueError("Unexpected style: '%s'" % style)
            style_converted = style_map[style]
            if style_converted is not None:
                new_style_collection.append(style_converted)
        element.style_collection = new_style_collection
