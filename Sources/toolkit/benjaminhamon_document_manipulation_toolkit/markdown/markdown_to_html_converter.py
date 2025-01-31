import re

import lxml.etree
import markdown


class MarkdownToHtmlConverter:


    def convert_metadata(self, metadata_as_markdown: str) -> dict:
        raise NotImplementedError


    def convert_content(self, content_as_markdown: str) -> str:
        document_lines = content_as_markdown.lstrip().splitlines()

        if document_lines[0] == "---":
            try:
                yaml_end_index = document_lines.index("---", 1)
            except ValueError as exception:
                raise ValueError("Document has an invalid YAML header") from exception

            content_as_markdown = "\n".join(document_lines[yaml_end_index + 1 :]).strip()

        html_root = lxml.etree.Element("html")
        html_body = lxml.etree.Element("body")
        html_root.append(html_body)

        if not content_as_markdown.startswith("#"):
            raise ValueError("Document should start with heading")

        document_as_html_string = "<html><body>" + self._convert_section_to_html(content_as_markdown, 0) + "</body></html>"
        document_as_html_string = document_as_html_string.replace("<strong><em>", "<span class=\"bold italic\">")
        document_as_html_string = document_as_html_string.replace("</em></strong>", "</span>")
        document_as_html_string = document_as_html_string.replace("<strong>", "<span class=\"bold\">")
        document_as_html_string = document_as_html_string.replace("</strong>", "</span>")
        document_as_html_string = document_as_html_string.replace("<em>", "<span class=\"italic\">")
        document_as_html_string = document_as_html_string.replace("</em>", "</span>")

        return document_as_html_string


    def _convert_section_to_html(self, section_as_markdown: str, heading_level: int) -> str:
        subsection_heading_match_collection = list(re.finditer(r"^#{" + str(heading_level + 1) +r"} ", section_as_markdown, flags = re.MULTILINE))

        first_subsection_match = next((x for x in subsection_heading_match_collection), None)
        section_text_end_index = first_subsection_match.start() if first_subsection_match is not None else len(section_as_markdown)

        section_as_html_string = markdown.markdown(section_as_markdown[:section_text_end_index])

        for heading_match, next_heading_match in zip(subsection_heading_match_collection, subsection_heading_match_collection[1:] + [ None ]):
            start_index = heading_match.start()
            end_index = next_heading_match.start() if next_heading_match is not None else len(section_as_markdown)

            subsection_data = section_as_markdown[start_index:end_index]
            section_as_html_string += self._convert_section_to_html(subsection_data, heading_level + 1)

        return "<section>" + section_as_html_string + "</section>" if heading_level != 0 else section_as_html_string
