from typing import List

from benjaminhamon_document_manipulation_toolkit.documents.elements.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.elements.text_element import TextElement


class DocumentToMarkdownConverter:


    def __init__(self) -> None:
        self.heading_top_margin = 2


    def convert_content(self, title: str, root: RootElement) -> str:
        content_as_markdown_lines: List[str] = []
        content_as_markdown_lines.append("# " + title)
        content_as_markdown_lines.extend([ "" ] * (self.heading_top_margin + 1))

        for section in root.enumerate_sections():
            content_as_markdown_lines.extend(self._convert_section(section, level = 2))

        return "\n".join(content_as_markdown_lines).rstrip() + "\n"


    def convert_content_as_section(self, section_element: SectionElement) -> str:
        content_as_markdown_lines: List[str] = []
        content_as_markdown_lines.extend(self._convert_section(section_element, level = 1))
        return "\n".join(content_as_markdown_lines).rstrip() + "\n"


    def _convert_section(self, section_element: SectionElement, level: int) -> List[str]:
        section_as_markdown_lines: List[str] = []
        section_as_markdown_lines.extend(self._convert_heading(section_element.get_heading(), level))

        for paragraph in section_element.enumerate_paragraphs():
            section_as_markdown_lines.extend(self._convert_paragraph(paragraph))
        section_as_markdown_lines.extend([ "" ] * self.heading_top_margin)

        for subsection in section_element.enumerate_subsections():
            section_as_markdown_lines.extend(self._convert_section(subsection, level + 1))

        return section_as_markdown_lines


    def _convert_heading(self, heading_element: HeadingElement, level: int) -> List[str]:
        heading_as_markdown_lines: List[str] = []

        heading_text_as_markdown = "#" * level
        for text in heading_element.enumerate_text():
            heading_text_as_markdown += " " + text.text
        heading_as_markdown_lines.append(heading_text_as_markdown)

        heading_as_markdown_lines.append("")

        return heading_as_markdown_lines


    def _convert_paragraph(self, paragraph_element: ParagraphElement) -> List[str]:
        paragraph_spans: List[str] = []
        for text_element in paragraph_element.enumerate_text():
            paragraph_spans.append(self._convert_text(text_element))

        paragraph_as_markdown = self._apply_styles(" ".join(paragraph_spans), paragraph_element.style_collection)

        return [ paragraph_as_markdown, "" ]


    def _convert_text(self, text_element: TextElement) -> str:
        raw_text = text_element.text
        if raw_text is None:
            return ""

        return self._apply_styles(raw_text, text_element.style_collection)


    def _apply_styles(self, text: str, style_collection: List[str]) -> str:
        style_tag = ""
        if "italic" in style_collection:
            style_tag += "*"
        if "bold" in style_collection:
            style_tag += "**"

        return style_tag + text + style_tag
