from typing import List

from benjaminhamon_document_manipulation_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.text_element import TextElement


def create_section(heading: str, text: List[List[str]]) -> SectionElement:
    section_element = SectionElement()
    section_element.children.append(create_heading(heading))

    for paragraph in text:
        section_element.children.append(create_paragraph(paragraph))

    return section_element


def create_heading(text: str) -> HeadingElement:
    heading_element = HeadingElement()
    text_element = TextElement(text)
    heading_element.children.append(text_element)

    return heading_element


def create_paragraph(text: List[str]) -> ParagraphElement:
    paragraph_element = ParagraphElement()

    for span in text:
        text_element = TextElement(span)
        paragraph_element.children.append(text_element)

    return paragraph_element
