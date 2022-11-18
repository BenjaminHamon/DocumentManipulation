import io

from bhamon_book_distribution_toolkit.documents.document import Document
from bhamon_book_distribution_toolkit.documents.section_element import SectionElement
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement


class MarkdownWriter:


	def write_document(self, stream: io.TextIOWrapper, document: Document) -> None:
		stream.write("# %s" % document.title + "\n\n\n")

		for section in document.content.sections:
			self.write_section(stream, section, level = 1)


	def write_section(self, stream: io.TextIOWrapper, section: SectionElement, level: int) -> None:
		stream.write("%s %s" % ("#" * (level + 1), section.title) + "\n\n")

		for paragraph in section.paragraphs:
			self.write_paragraph(stream, paragraph)

		for subsection in section.sections:
			self.write_section(stream, subsection, level + 1)

		stream.write("\n")


	def write_paragraph(self, stream: io.TextIOWrapper, paragraph_element: ParagraphElement) -> None:
		for text_element in paragraph_element.text_elements:
			stream.write(text_element.text)
		stream.write("\n\n")
