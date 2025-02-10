import logging
import os
from typing import Mapping

from benjaminhamon_document_manipulation_toolkit.documents import document_operations
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.markdown.document_to_markdown_converter import DocumentToMarkdownConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


logger = logging.getLogger("MarkdownWriter")


class MarkdownWriter:


    def __init__(self, converter: DocumentToMarkdownConverter, serializer: Serializer) -> None:
        self._converter = converter
        self._serializer = serializer
        self.encoding = "utf-8"


    def write_to_file(self, output_file_path: str, document: str, simulate: bool = False) -> None:
        logger.debug("Writing '%s'", output_file_path)

        if not simulate:
            with open(output_file_path + ".tmp", mode = "w", encoding = self.encoding) as output_file:
                output_file.write(document)
            os.replace(output_file_path + ".tmp", output_file_path)


    def write_as_single_document(self, # pylint: disable = too-many-arguments
            output_file_path: str, title: str, metadata: Mapping[str,str], content: RootElement, simulate: bool = False) -> None:

        document_as_markdown = ""

        if len(metadata) > 0:
            document_as_markdown += "---" + "\n"
            document_as_markdown += self._serializer.serialize_to_string(metadata)
            document_as_markdown += "---" + "\n"
            document_as_markdown += "\n" * (self._converter.heading_top_margin + 1)

        document_as_markdown += self._converter.convert_content(title, content)

        self.write_to_file(output_file_path, document_as_markdown, simulate = simulate)


    def write_as_many_documents(self, # pylint: disable = too-many-arguments
            output_directory: str, metadata: Mapping[str,str], content: RootElement, simulate: bool = False) -> None:

        section_count = content.get_section_count()

        if len(metadata) > 0:
            section_index = -1

            metadata_as_markdown = self._serializer.serialize_to_string(metadata)

            file_name = document_operations.generate_section_file_name("Information", section_index, section_count)
            output_file_path = os.path.join(output_directory, file_name + self._serializer.get_file_extension())

            self.write_to_file(output_file_path, metadata_as_markdown, simulate = simulate)

        for section_index, section in enumerate(content.enumerate_sections()):
            title = section.get_heading().get_title()
            section_as_markdown = self._converter.convert_content_as_section(section)

            file_name = document_operations.generate_section_file_name(title, section_index, section_count)
            markdown_file_path = os.path.join(output_directory, file_name + ".md")

            self.write_to_file(markdown_file_path, section_as_markdown, simulate = simulate)
