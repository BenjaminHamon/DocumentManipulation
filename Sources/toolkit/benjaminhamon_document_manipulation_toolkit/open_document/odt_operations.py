# cspell:words fodt getroottree iterchildren lxml nsmap

import zipfile
import lxml.etree

from benjaminhamon_document_manipulation_toolkit.open_document import odt_namespaces
from benjaminhamon_document_manipulation_toolkit.xml import xpath_helpers


def create_document() -> lxml.etree._ElementTree:
    namespaces = {
        "dc": odt_namespaces.dc_namespace,
        "draw": odt_namespaces.draw_namespace,
        "office": odt_namespaces.office_namespace,
        "text": odt_namespaces.text_namespace,
    }

    document_element = lxml.etree.Element(lxml.etree.QName(namespaces["office"], "document"), nsmap = namespaces)
    body_element = lxml.etree.SubElement(document_element, lxml.etree.QName(namespaces["office"], "body"))
    lxml.etree.SubElement(body_element, lxml.etree.QName(namespaces["office"], "text"))
    return lxml.etree.ElementTree(document_element)


def load_document(xml_parser: lxml.etree.XMLParser, template_file_path: str) -> lxml.etree._ElementTree:
    document = load_document_raw(xml_parser, template_file_path)

    body_text_element = get_body_text_element(document)
    if body_text_element.text is not None:
        if body_text_element.text == "" or body_text_element.text.isspace():
            body_text_element.text = None

    return document


def load_document_raw(xml_parser: lxml.etree.XMLParser, template_file_path: str) -> lxml.etree._ElementTree:
    if template_file_path.endswith(".fodt"):
        return lxml.etree.parse(template_file_path, xml_parser)

    if template_file_path.endswith(".odt"):
        with zipfile.ZipFile(template_file_path, mode = "r") as odt_file:
            odt_content = odt_file.read("content.xml")
        return lxml.etree.fromstring(odt_content).getroottree()

    raise ValueError("Unsupported file: '%s'" % template_file_path)


def get_body_text_element(xml_document: lxml.etree._ElementTree) -> lxml.etree._Element:
    return xpath_helpers.find_xml_element(xml_document.getroot(), "./office:body/office:text", xml_document.getroot().nsmap)


def remove_content(xml_document: lxml.etree._ElementTree) -> None:
    body_text_element = get_body_text_element(xml_document)

    for element in list(body_text_element.iterchildren()):
        body_text_element.remove(element)
