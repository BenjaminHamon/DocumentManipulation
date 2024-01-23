# cspell:words dateutil fodt localname lxml nsmap

import datetime
from typing import Dict, List, Optional
import zipfile

import dateutil.parser
import lxml.etree

from benjaminhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_book_distribution_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_book_distribution_toolkit.documents.root_element import RootElement
from benjaminhamon_book_distribution_toolkit.documents.section_element import SectionElement
from benjaminhamon_book_distribution_toolkit.documents.text_element import TextElement
from benjaminhamon_book_distribution_toolkit.xml import xpath_helpers


class OdtReader:


    def __init__(self, xml_parser: lxml.etree.XMLParser) -> None:
        self._xml_parser = xml_parser


    def read_fodt(self, odt_file_path: str) -> bytes:
        with open(odt_file_path, mode = "rb") as fodt_file:
            return fodt_file.read()


    def read_odt(self, odt_file_path: str, content_file_path: str) -> bytes:
        with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
            return odt_file.read(content_file_path)


    def read_metadata(self, odt_as_bytes: bytes) -> dict:
        odt_as_xml = lxml.etree.fromstring(odt_as_bytes, self._xml_parser)
        metadata_as_xml = odt_as_xml.find("office:meta", namespaces = odt_as_xml.nsmap) # type: ignore

        if metadata_as_xml is None:
            raise ValueError("Metadata element not found")

        metadata = {}

        for item_as_xml in metadata_as_xml.iter():
            key = lxml.etree.QName(item_as_xml).localname
            value = item_as_xml.text

            if key == "meta" or value is None:
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


    def read_content(self, odt_as_bytes: bytes) -> RootElement:
        odt_as_xml = lxml.etree.fromstring(odt_as_bytes, self._xml_parser)

        self._strip_comments(odt_as_xml)
        self._strip_layout_elements(odt_as_xml)

        body_as_xml = xpath_helpers.find_xml_element(odt_as_xml, "office:body/office:text", odt_as_xml.nsmap)
        text_elements = xpath_helpers.try_find_xml_element_collection(body_as_xml, "//*[self::text:h or self::text:p]", odt_as_xml.nsmap)

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


    def _strip_comments(self, odt_as_xml: lxml.etree._Element) -> None:
        element_tags = [
            lxml.etree.QName(odt_as_xml.nsmap["office"], "annotation"),
            lxml.etree.QName(odt_as_xml.nsmap["office"], "annotation-end"),
        ]

        lxml.etree.strip_elements(odt_as_xml, *element_tags, with_tail = False)


    def _strip_layout_elements(self, odt_as_xml: lxml.etree._Element) -> None:
        element_tags = [
            lxml.etree.QName(odt_as_xml.nsmap["text"], "s"),
            lxml.etree.QName(odt_as_xml.nsmap["text"], "soft-page-break"),
        ]

        lxml.etree.strip_elements(odt_as_xml, *element_tags, with_tail = False)



    def _convert_section_element(self, section_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> SectionElement:
        section_element = SectionElement()

        heading_element = HeadingElement()
        heading_element.style_collection = self._get_styles_from_element(section_as_xml, namespaces)
        heading_element.children.extend(self._get_text(section_as_xml, namespaces))

        section_element.children.append(heading_element)

        return section_element


    def _convert_paragraph_element(self, paragraph_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> ParagraphElement:
        paragraph_element = ParagraphElement()
        paragraph_element.style_collection = self._get_styles_from_element(paragraph_as_xml, namespaces)
        paragraph_element.children.extend(self._get_text(paragraph_as_xml, namespaces))

        return paragraph_element


    def _get_text(self, text_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> List[TextElement]:

        # A text XML element from an ODT document will directly contain raw text,
        # but it may also contain child elements such as spans and breaks, and then raw text as tails.
        # e.g. <p>text <span>italic</span> text</p> or <p>text <soft-page-break/>text</p>

        all_text_elements: List[TextElement] = []

        for current_xml_element in text_as_xml.iter(None):
            tag = lxml.etree.QName(current_xml_element).localname

            if tag not in ( "a", "h", "p", "span", "line-break" ):
                raise ValueError("Unsupported text tag: '%s'" % tag)

            if tag == "line-break":
                all_text_elements[-1].line_break = True

            if current_xml_element.text is not None:
                if tag in ( "h", "p" ):
                    text_element = TextElement(current_xml_element.text.strip())
                    all_text_elements.append(text_element)

                if tag in ( "a", "span" ):
                    text_element = TextElement(current_xml_element.text.strip())
                    text_element.style_collection = self._get_styles_from_element(current_xml_element, namespaces)
                    all_text_elements.append(text_element)

            if current_xml_element.tail is not None and not current_xml_element.tail.isspace():
                if tag in ( "a", "h", "p", "span", "line-break" ):
                    text_element = TextElement(current_xml_element.tail.strip())
                    all_text_elements.append(text_element)

        return all_text_elements


    def _get_styles_from_element(self, element_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> List[str]:
        style_collection = []

        style_name_attribute_key = lxml.etree.QName(namespaces["text"], "style-name")
        odt_style = element_as_xml.attrib.get(str(style_name_attribute_key))
        if odt_style is not None:
            style_collection.append(str(odt_style).replace("_20_", " ")) # Spaces in style names are stored as "_20_"

        return style_collection
