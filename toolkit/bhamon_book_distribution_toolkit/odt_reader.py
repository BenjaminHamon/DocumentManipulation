from typing import Dict, Optional
import zipfile

import lxml.etree

from bhamon_book_distribution_toolkit.documents.document_content import DocumentContent
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from bhamon_book_distribution_toolkit.documents.section_element import SectionElement
from bhamon_book_distribution_toolkit.documents.text_element import TextElement


class OdtReader:


	def __init__(self, style_map: Dict[str, str]) -> None:
		self._parser = lxml.etree.XMLParser(encoding = "utf-8")
		self._style_map = style_map


	def read_odt(self, odt_file_path: str) -> bytes:
		if odt_file_path.endswith(".fodt"):
			with open(odt_file_path, mode = "rb") as fodt_file:
				return fodt_file.read()

		with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
			return odt_file.read("content.xml")


	def read_document_content(self, odt_content: bytes) -> DocumentContent:
		odt_as_xml = lxml.etree.fromstring(odt_content, self._parser)
		body_xml = odt_as_xml.find("office:body/office:text", namespaces = odt_as_xml.nsmap)
		text_elements = body_xml.xpath("//*[self::text:h or self::text:p]", namespaces = odt_as_xml.nsmap)

		document_content = DocumentContent()
		current_section = None

		for element in text_elements:
			tag = lxml.etree.QName(element).localname

			if tag == "h":
				current_section = self._convert_section_element(element, odt_as_xml.nsmap)
				document_content.sections.append(current_section)

			if tag == "p":
				if current_section is None:
					continue

				current_section.paragraphs.append(self._convert_paragraph_element(element, odt_as_xml.nsmap))

		return document_content


	def _convert_section_element(self, section_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> SectionElement:
		style = self._get_style_from_element(section_as_xml, namespaces)
		text = section_as_xml.xpath("string()")
		
		return SectionElement(title = text, style = style)


	def _convert_paragraph_element(self, paragraph_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> ParagraphElement:
		style = self._get_style_from_element(paragraph_as_xml, namespaces)
		paragraph_element = ParagraphElement(style = style)

		for text_as_xml in paragraph_as_xml.iter():
			style = self._get_style_from_element(text_as_xml, namespaces)
			text_element = TextElement(text_as_xml.text, style = style)
			if text_element.text is None:
				text_element.text = ""
			paragraph_element.text_elements.append(text_element)
		
		return paragraph_element


	def _get_style_from_element(self, element_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> Optional[str]:
		attribute = next((x for x in element_as_xml.xpath('@text:style-name', namespaces = namespaces)), None)
		if attribute is None:
			return None

		style_identifier = attribute.replace("_20_", " ")
		return self._style_map.get(style_identifier, None)
