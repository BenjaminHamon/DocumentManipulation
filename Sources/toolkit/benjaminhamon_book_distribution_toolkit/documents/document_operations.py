from typing import Iterator

from benjaminhamon_book_distribution_toolkit import convert_helpers
from benjaminhamon_book_distribution_toolkit.documents.document_element import DocumentElement


def enumerate_all_elements(element: DocumentElement) -> Iterator[DocumentElement]:
    yield element

    for child in element.children:
        yield from enumerate_all_elements(child)


def generate_section_file_name(section_title: str, section_index: int, section_count: int) -> str:
    title = str(section_index + 1).rjust(len(str(section_count)), "0") + " - " + section_title
    return convert_helpers.sanitize_for_file_name(title)
