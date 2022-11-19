import datetime
from typing import Dict, List, Optional
import zipfile

import dateutil.parser
import lxml.etree

from bhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from bhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from bhamon_book_distribution_toolkit.documents.root_element import RootElement
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


	def read_document_content(self, odt_content: bytes) -> RootElement:
		odt_as_xml = lxml.etree.fromstring(odt_content, self._xml_parser)
		body_xml = odt_as_xml.find("office:body/office:text", namespaces = odt_as_xml.nsmap)
		text_elements = body_xml.xpath("//*[self::text:h or self::text:p]", namespaces = odt_as_xml.nsmap)

		root_element = RootElement()
		root_element.identifier = "root"

		current_section = None

		for element in text_elements:
			tag = lxml.etree.QName(element).localname

			if tag == "h":
				current_section = self._convert_section_element(element, odt_as_xml.nsmap)
				root_element.children.append(current_section)

			if tag == "p":
				if current_section is None:
					continue

				current_section.children.append(self._convert_paragraph_element(element, odt_as_xml.nsmap))

		return root_element


	def _convert_section_element(self, section_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> SectionElement:
		section_element = SectionElement()

		heading_element = HeadingElement()
		heading_element.style_collection = self._get_styles_from_element(section_as_xml, namespaces)

		text_element = TextElement()
		text_element.text = section_as_xml.xpath("string()")

		heading_element.children.append(text_element)
		section_element.children.append(heading_element)
		
		return section_element


	def _convert_paragraph_element(self, paragraph_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> ParagraphElement:
		paragraph_element = ParagraphElement()
		paragraph_element.style_collection = self._get_styles_from_element(paragraph_as_xml, namespaces)

		for text_as_xml in paragraph_as_xml.iter():
			is_new_text_element = lxml.etree.QName(text_as_xml).localname in [ "p", "span" ] or len(paragraph_element.children) == 0

			if is_new_text_element:
				if text_as_xml.text is not None:
					text_element = TextElement()
					text_element.text = text_as_xml.text.strip()
					if lxml.etree.QName(text_as_xml).localname == "span":
						text_element.style_collection = self._get_styles_from_element(text_as_xml, namespaces)
					paragraph_element.children.append(text_element)

				if text_as_xml.tail is not None:
					text_element = TextElement()
					text_element.text = text_as_xml.tail.strip()
					paragraph_element.children.append(text_element)

			if not is_new_text_element:
				if text_as_xml.tail is not None:
					paragraph_element.children[-1].text += " " + text_as_xml.tail.strip()
		
		return paragraph_element


	def _get_styles_from_element(self, element_as_xml: lxml.etree.ElementBase, namespaces: Dict[str,str]) -> List[str]:
		style_collection = []

		odt_style = element_as_xml.attrib.get(lxml.etree.QName(namespaces["text"], "style-name"))
		if odt_style is not None:
			odt_style = odt_style.replace("_20_", " ")

			known_style = self._style_map.get(odt_style, None)
			if known_style is not None:
				style_collection.append(known_style)

		return style_collection
