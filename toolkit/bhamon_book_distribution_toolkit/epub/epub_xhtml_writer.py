from typing import List
import lxml.etree

from bhamon_book_distribution_toolkit.documents.document_element import DocumentElement
from bhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from bhamon_book_distribution_toolkit.documents.section_element import SectionElement
from bhamon_book_distribution_toolkit.documents.text_element import TextElement


class EpubXhtmlWriter:

	
	def __init__(self) -> None:
		self.pretty_print = True
		self.encoding = "utf-8"


	def write_xhtml_file(self, xhtml_file_path: str, xhtml_content: lxml.etree.ElementTree) -> None:
		xhtml_content.write(xhtml_file_path,
			xml_declaration = True,
			doctype = "<!doctype html>",
			pretty_print = self.pretty_print,
			encoding = self.encoding)


	def create_xhtml_from_section(self, section: SectionElement, all_stylesheet_links: List[str]) -> lxml.etree.ElementTree:
		namespaces = {
			None: "http://www.w3.org/1999/xhtml",
			"epub": "http://www.idpf.org/2007/ops",
		}

		root_element = lxml.etree.Element("html", nsmap = namespaces)
		
		head_element = lxml.etree.SubElement(root_element, "head")
		title_element = lxml.etree.SubElement(head_element, "title")
		title_element.text = section.get_heading().get_text().text

		for stylesheet in all_stylesheet_links:
			lxml.etree.SubElement(head_element, "link", rel = "stylesheet", href = stylesheet)

		body_element = lxml.etree.SubElement(root_element, "body")
		body_element.append(self._convert_section_to_html(section, level = 1))

		return lxml.etree.ElementTree(root_element)


	def _convert_section_to_html(self, section: SectionElement, level: int) -> lxml.etree.Element:
		section_as_html = lxml.etree.Element("section" if level == 1 else "div", self._get_html_attributes_from_element(section))

		section_as_html.append(self._convert_heading_to_html(section.get_heading()))

		for paragraph in section.enumerate_paragraphs():
			section_as_html.append(self._convert_paragraph_to_html(paragraph))

		for subsection in section.enumerate_subsections():
			section_as_html.append(self._convert_section_to_html(subsection, level + 1))

		return section_as_html


	def _convert_heading_to_html(self, heading: HeadingElement) -> lxml.etree.Element:
		heading_as_html = lxml.etree.Element("h" + str(heading.level_in_tree), self._get_html_attributes_from_element(heading))

		prefix_as_html = lxml.etree.SubElement(heading_as_html, "span")
		if heading.category is not None:
			prefix_as_html.text = heading.category
			if heading.index_in_category is not None:
				prefix_as_html.text += " " + str(heading.index_in_category)

		text_as_html = lxml.etree.SubElement(heading_as_html, "span")
		text_as_html.text = heading.get_text().text

		return heading_as_html


	def _convert_paragraph_to_html(self, paragraph_element: ParagraphElement) -> lxml.etree.Element:
		paragraph_as_html = lxml.etree.Element("p", self._get_html_attributes_from_element(paragraph_element))

		for text_element in paragraph_element.enumerate_text():
			paragraph_as_html.append(self._convert_text_to_html(text_element))

		return paragraph_as_html


	def _convert_text_to_html(self, text_element: TextElement) -> lxml.etree.Element:
		text_as_html = lxml.etree.Element("span", self._get_html_attributes_from_element(text_element))
		text_as_html.text = text_element.text

		if text_as_html.text is None or text_as_html == "":
			text_as_html.text = "\u00a0" # no-break space

		return text_as_html


	def _get_html_attributes_from_element(self, element: DocumentElement) -> dict:
		attributes = {}

		if element.identifier is not None:
			attributes["id"] = element.identifier
		if len(element.style_collection) > 0:
			attributes["class"] = " ".join(element.style_collection)

		return attributes
