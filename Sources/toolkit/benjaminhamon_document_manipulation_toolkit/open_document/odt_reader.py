# cspell:words dateutil fodt localname lxml nsmap

import datetime
from typing import Dict, List, Optional
import zipfile

import dateutil.parser
import lxml.etree

from benjaminhamon_document_manipulation_toolkit.documents.document_comment import DocumentComment
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
        self._region_counter: int = 0


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
        self._region_counter = 0

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


    def read_comments(self, odt_as_bytes: bytes) -> List[DocumentComment]:
        self._region_counter = 0

        odt_as_xml = lxml.etree.fromstring(odt_as_bytes, self._xml_parser)

        body_as_xml = xpath_helpers.find_xml_element(odt_as_xml, "office:body/office:text", odt_as_xml.nsmap)
        all_annotation_elements = xpath_helpers.try_find_xml_element_collection(body_as_xml, "//*[self::office:annotation]", odt_as_xml.nsmap)

        all_comments: List[DocumentComment] = []
        for element in all_annotation_elements:
            all_comments.append(self._convert_comment_element(element, odt_as_xml.nsmap))

        return all_comments


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


    def _convert_comment_element(self, comment_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> DocumentComment:
        region_identifier = self._get_region_identifier_from_element(comment_as_xml, namespaces)

        creator_element = xpath_helpers.find_xml_element(comment_as_xml, "./dc:creator", namespaces)
        if creator_element.text is None:
            raise ValueError("Creator element is empty")
        author = creator_element.text

        date_element = xpath_helpers.find_xml_element(comment_as_xml, "./dc:date", namespaces)
        if date_element.text is None:
            raise ValueError("Date element is empty")
        date = dateutil.parser.parse(date_element.text).replace(microsecond = 0)

        text = ""
        all_text_elements = xpath_helpers.try_find_xml_element_collection(comment_as_xml, "./text:p", namespaces)
        for text_element in all_text_elements:
            text += "".join(str(x) for x in text_element.itertext() if x is not None) + "\n"
        text = text.strip()

        self._region_counter += 1

        return DocumentComment(region_identifier, author, date, text)


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
                    text_element = TextElement(current_xml_element.text)
                    all_text_elements.append(text_element)
                    previous_text_element = text_element

                if tag in ( "a", "span" ):
                    text_element = TextElement(current_xml_element.text)
                    text_element.style_collection = self._get_styles_from_element(current_xml_element, namespaces)
                    all_text_elements.append(text_element)
                    previous_text_element = text_element

            if tag in ( "annotation", "annotation-end"):
                region_identifier = self._get_region_identifier_from_element(current_xml_element, namespaces)

                if tag == "annotation":
                    text_location_element = TextRegionStartElement(region_identifier)
                    all_text_elements.append(text_location_element)
                    self._region_counter += 1

                if tag == "annotation-end":
                    text_location_element = TextRegionEndElement(region_identifier)
                    all_text_elements.append(text_location_element)

            if current_xml_element.tail is not None and not current_xml_element.tail.isspace():
                text_element = TextElement(current_xml_element.tail)
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


    def _get_region_identifier_from_element(self, element_as_xml: lxml.etree._Element, namespaces: Dict[Optional[str], str]) -> str:
        region_identifier_attribute_key = lxml.etree.QName(namespaces["office"], "name")
        region_identifier = element_as_xml.attrib.get(str(region_identifier_attribute_key))
        if region_identifier is not None:
            return str(region_identifier)
        return "AnnotationWithoutName_" + str(self._region_counter)
