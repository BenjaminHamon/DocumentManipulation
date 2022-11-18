import lxml.etree

from bhamon_book_distribution_toolkit.documents.section_element import SectionElement
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement


class EpubXhtmlWriter:

	
	def __init__(self) -> None:
		self.pretty_print = True
		self.encoding = "utf-8"


	def write_section_as_file(self, xhtml_file_path: str, section: SectionElement) -> None:
		xhtml_content = self.create_xhtml_from_section(section)

		xhtml_content.write(xhtml_file_path,
			xml_declaration = True,
			doctype = "<!doctype html>",
			pretty_print = self.pretty_print,
			encoding = self.encoding)


	def create_xhtml_from_section(self, section: SectionElement) -> lxml.etree.ElementTree:
		namespaces = {
			None: "http://www.w3.org/1999/xhtml",
			"epub": "http://www.idpf.org/2007/ops",
		}

		root_element = lxml.etree.Element("html", nsmap = namespaces)
		
		head_element = lxml.etree.SubElement(root_element, "head")
		title_element = lxml.etree.SubElement(head_element, "title")
		title_element.text = section.title

		body_element = lxml.etree.SubElement(root_element, "body")
		body_element.append(self._convert_section_to_html(section, level = 1))

		return lxml.etree.ElementTree(root_element)


	def _convert_section_to_html(self, section: SectionElement, level: int) -> lxml.etree.Element:
		section_element = lxml.etree.Element("section" if level == 1 else "div")

		header_element = lxml.etree.SubElement(section_element, "h" + str(level))
		header_element.text = section.title

		for paragraph in section.paragraphs:
			section_element.append(self._convert_paragraph_to_html(paragraph))

		for subsection in section.sections:
			section_element.append(self._convert_section_to_html(subsection, level + 1))

		return section_element


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
