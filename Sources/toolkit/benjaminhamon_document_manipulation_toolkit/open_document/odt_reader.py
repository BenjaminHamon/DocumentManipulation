# cspell:words dateutil fodt localname lxml nsmap

import datetime
from typing import Dict, List, Optional
import zipfile

import dateutil.parser
import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.document_element import DocumentElement
from benjaminhamon_document_manipulation_toolkit.documents.heading_element import HeadingElement
from benjaminhamon_document_manipulation_toolkit.documents.paragraph_element import ParagraphElement
from benjaminhamon_document_manipulation_toolkit.documents.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.documents.section_element import SectionElement
from benjaminhamon_document_manipulation_toolkit.documents.text_element import TextElement
from benjaminhamon_document_manipulation_toolkit.documents.text_region_end_element import TextRegionEndElement
from benjaminhamon_document_manipulation_toolkit.documents.text_region_start_element import TextRegionStartElement
from benjaminhamon_document_manipulation_toolkit.xml import xpath_helpers


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

        self._strip_annotation_data(odt_as_xml)
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


    def _strip_annotation_data(self, odt_as_xml: lxml.etree._Element) -> None:
        all_annotation_elements = xpath_helpers.try_find_xml_element_collection(
            odt_as_xml, "//*[self::office:annotation or self::office:annotation-end]", odt_as_xml.nsmap)

        for annotation_element in all_annotation_elements:
            for annotation_element_child in list(annotation_element):
                annotation_element.remove(annotation_element_child)


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


    def _get_text(self, text_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> List[DocumentElement]:

        # A text XML element from an ODT document will directly contain raw text,
        # but it may also contain child elements such as spans and breaks, and then raw text as tails.
        # e.g. <p>text <span>italic</span> text</p> or <p>text <soft-page-break/>text</p>

        all_text_elements: List[DocumentElement] = []
        previous_text_element: Optional[TextElement] = None

        for current_xml_element in text_as_xml.iter(None):
            tag = lxml.etree.QName(current_xml_element).localname

            if tag not in ( "a", "h", "p", "span", "line-break", "annotation", "annotation-end" ):
                raise ValueError("Unsupported text tag: '%s'" % tag)

            if tag == "line-break" and previous_text_element is not None:
                previous_text_element.line_break = True

            if current_xml_element.text is not None:
                if tag in ( "h", "p" ):
                    text_element = TextElement(current_xml_element.text.strip())
                    all_text_elements.append(text_element)
                    previous_text_element = text_element

                if tag in ( "a", "span" ):
                    text_element = TextElement(current_xml_element.text.strip())
                    text_element.style_collection = self._get_styles_from_element(current_xml_element, namespaces)
                    all_text_elements.append(text_element)
                    previous_text_element = text_element

            if tag in ( "annotation", "annotation-end"):
                comment_identifier = self._get_location_identifier_from_element(current_xml_element, namespaces)

                if tag == "annotation":
                    text_location_element = TextRegionStartElement(comment_identifier)
                    all_text_elements.append(text_location_element)

                if tag == "annotation-end":
                    text_location_element = TextRegionEndElement(comment_identifier)
                    all_text_elements.append(text_location_element)

            if current_xml_element.tail is not None and not current_xml_element.tail.isspace():
                text_element = TextElement(current_xml_element.tail.strip())
                all_text_elements.append(text_element)
                previous_text_element = text_element

        return all_text_elements


    def _get_styles_from_element(self, element_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> List[str]:
        style_collection = []

        style_name_attribute_key = lxml.etree.QName(namespaces["text"], "style-name")
        odt_style = element_as_xml.attrib.get(str(style_name_attribute_key))
        if odt_style is not None:
            style_collection.append(str(odt_style).replace("_20_", " ")) # Spaces in style names are stored as "_20_"

        return style_collection


    def _get_location_identifier_from_element(self, element_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> str:
        comment_identifier_attribute_key = lxml.etree.QName(namespaces["office"], "name")
        comment_identifier = element_as_xml.attrib.get(str(comment_identifier_attribute_key))
        if comment_identifier is None:
            raise ValueError("Annotation element is missing an identifier attribute (office:name)")
        return str(comment_identifier)
