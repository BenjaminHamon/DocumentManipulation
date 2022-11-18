import datetime
from typing import Dict, Optional
import zipfile

import dateutil.parser
import lxml.etree

from bhamon_book_distribution_toolkit.documents.document_content import DocumentContent
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from bhamon_book_distribution_toolkit.documents.section_element import SectionElement
from bhamon_book_distribution_toolkit.documents.text_element import TextElement


class OdtReader:


	def __init__(self, xml_parser: lxml.etree.XMLParser, style_map: Dict[str,str]) -> None:
		self._xml_parser = xml_parser
		self._style_map = style_map


	def read_fodt(self, odt_file_path: str) -> bytes:
		with open(odt_file_path, mode = "rb") as fodt_file:
			return fodt_file.read()


	def read_odt(self, odt_file_path: str, content_file_path: str) -> bytes:
		with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
			return odt_file.read(content_file_path)


	def read_metadata(self, odt_content: bytes) -> dict:
		odt_as_xml = lxml.etree.fromstring(odt_content, self._xml_parser)
		metatada_as_xml = odt_as_xml.find("office:meta", namespaces = odt_as_xml.nsmap)
		metadata = {}

		for item_as_xml in metatada_as_xml.iter():
			key = lxml.etree.QName(item_as_xml).localname
			value = item_as_xml.text

			if key == "meta":
				continue

			if key == "title":
				metadata["title"] = value

			if key == "creator":
				metadata["author"] = value

			if key == "creation-date":
				metadata["creation_date"] = dateutil.parser.parse(value).astimezone(datetime.timezone.utc).replace(microsecond = 0)

			if key == "date":
				metadata["update_date"] = dateutil.parser.parse(value).astimezone(datetime.timezone.utc).replace(microsecond = 0)

			if key == "editing-cycles":
				metadata["revision"] = int(value)

			if key == "user-defined":
				continue

		return metadata


	def read_document_content(self, odt_content: bytes) -> DocumentContent:
		odt_as_xml = lxml.etree.fromstring(odt_content, self._xml_parser)
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
		paragraph_element = ParagraphElement()

		for text_as_xml in paragraph_as_xml.iter():
			is_new_text_element = lxml.etree.QName(text_as_xml).localname in [ "p", "span" ] or len(paragraph_element.text_elements) == 0

			if is_new_text_element:
				if text_as_xml.text is not None:
					style = self._get_style_from_element(text_as_xml, namespaces)
					text_element = TextElement(text_as_xml.text.strip(), style = style)
					paragraph_element.text_elements.append(text_element)

				if text_as_xml.tail is not None:
					text_element = TextElement(text_as_xml.tail.strip())
					paragraph_element.text_elements.append(text_element)

			if not is_new_text_element:
				if text_as_xml.tail is not None:
					paragraph_element.text_elements[-1].text += " " + text_as_xml.tail.strip()

		if len(paragraph_element.text_elements) == 0:
			text_element = TextElement("")
			paragraph_element.text_elements.append(text_element)
		
		return paragraph_element


	def _get_style_from_element(self, element_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> Optional[str]:
		attribute = next((x for x in element_as_xml.xpath('@text:style-name', namespaces = namespaces)), None)
		if attribute is None:
			return None

		style_identifier = attribute.replace("_20_", " ")
		return self._style_map.get(style_identifier, None)
