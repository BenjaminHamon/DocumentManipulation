import re
from typing import Optional

import jinja2
import lxml.etree
from ebooklib.epub import EpubBook
from ebooklib.epub import EpubItem
from ebooklib.epub import EpubHtml
from ebooklib.epub import EpubNav
from ebooklib.epub import EpubNcx

from bhamon_book_distribution_toolkit.documents.document import Document
from bhamon_book_distribution_toolkit.documents.section_element import SectionElement
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement


class EpubConverter:


	def __init__(self, jinja_environment: jinja2.Environment) -> None:
		self._jinja_environment = jinja_environment


	def convert_document(self,
			document: Document,
			annotation: Optional[str] = None,
			css_file_path: Optional[str] = None,
			front_page_template_path: Optional[str] = None) -> EpubBook:

		document_as_epub = EpubBook()
		document_as_epub.spine = []
		
		self._add_general_information(document, document_as_epub, annotation)

		if css_file_path is not None:
			with open(css_file_path) as css_file:
				css_data = css_file.read()

			style_as_epub = self.convert_style("document", css_data)
			document_as_epub.add_item(style_as_epub)

		if front_page_template_path is not None:
			template_parameters = {
				"title": document.title,
				"authors": document.authors,
				"annotation": annotation,
				"revision": document.revision,
				"revision_date": document.revision_date,
				"copyright": document.copyright.replace("(c)", "©"),
			}

			page_as_epub = self.convert_page("FrontPage", front_page_template_path, template_parameters)
			document_as_epub.add_item(page_as_epub)
			document_as_epub.spine.append(page_as_epub)

		document_as_epub.spine += [ "nav" ]

		for section in document.content.sections:
			section_as_epub = self.convert_section(section)
			document_as_epub.add_item(section_as_epub)
			document_as_epub.toc.append(section_as_epub)
			document_as_epub.spine.append(section_as_epub)

		document_as_epub.add_item(EpubNcx())
		document_as_epub.add_item(EpubNav())

		return document_as_epub


	def _add_general_information(self, document: Document, document_as_epub: EpubBook, annotation: Optional[str]) -> None:
		title = document.title
		if annotation is not None:
			title += " - " + annotation

		document_as_epub.set_title(title)

		for author in document.authors:
			document_as_epub.add_author(author)

		if document.identifier_for_epub is not None:
			document_as_epub.set_identifier(document.identifier_for_epub)
		if document.language is not None:
			document_as_epub.set_language(document.language)


	def convert_style(self, identifier: str, css_data: str) -> EpubItem:
		style_as_epub = EpubItem(
			uid = identifier,
			file_name = "styles" + "/" + self._sanitize_identifier(identifier) + ".css",
			media_type = "text/css")

		style_as_epub.content = css_data

		return style_as_epub


	def convert_page(self, identifier: str, template_file_path: str, parameters: dict) -> EpubHtml:
		page_as_epub = EpubHtml(
			title = identifier,
			file_name = "pages" + "/" + self._sanitize_identifier(identifier) + ".xhtml")

		page_as_epub.add_link(href = "../styles/document.css", rel = "stylesheet", type = "text/css")

		template = self._jinja_environment.get_template(template_file_path)
		page_as_epub.content = template.render(**parameters)

		return page_as_epub


	def convert_section(self, section: SectionElement) -> EpubHtml:
		section_as_epub = EpubHtml(
			title = section.title,
			file_name = "sections" + "/" + self._sanitize_identifier(section.title) + ".xhtml")

		section_as_epub.add_link(href = "../styles/document.css", rel = "stylesheet", type = "text/css")
		
		section_as_xml = self._convert_section_to_html(section, 1)
		section_as_xml_text = lxml.etree.tostring(section_as_xml, encoding = "utf-8").decode("utf-8")
		section_as_epub.content = section_as_xml_text

		return section_as_epub


	def _convert_section_to_html(self, section: SectionElement, level: int) -> lxml.etree.Element:
		element = lxml.etree.Element("h" + str(level))
		element.text = section.title

		for paragraph in section.paragraphs:
			element.append(self._convert_paragraph_to_html(paragraph))

		for subsection in section.sections:
			element.append(self._convert_section_to_html(subsection, level + 1))

		return element


	def _convert_paragraph_to_html(self, paragraph_element: ParagraphElement) -> lxml.etree.Element:
		attributes = {}
		if paragraph_element.style is not None:
			attributes["class"] = paragraph_element.style

		html_element = lxml.etree.Element("p", attributes)

		for text_element in paragraph_element.text_elements:
			html_element.append(self._convert_text_to_html(text_element))

		return html_element


	def _convert_text_to_html(self, text_element: ParagraphElement) -> lxml.etree.Element:
		attributes = {}
		if text_element.style is not None:
			attributes["class"] = text_element.style

		html_element = lxml.etree.Element("span", attributes)
		html_element.text = text_element.text

		if html_element.text == "":
			html_element.text = "\u00a0" # no-break space

		return html_element


	def _sanitize_identifier(self, identifier: str) -> str:
		return re.sub("[^a-zA-Z0-9]", "_", identifier)
