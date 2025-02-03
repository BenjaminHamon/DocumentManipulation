from typing import Dict, Iterator, Optional

from benjaminhamon_document_manipulation_toolkit import convert_helpers
from benjaminhamon_document_manipulation_toolkit.documents.elements.document_element import DocumentElement


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
