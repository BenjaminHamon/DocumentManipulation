# cspell:words lxml nsmap

from typing import Dict, List, Optional

import lxml.etree
import lxml.html

from benjaminhamon_document_manipulation_toolkit.epub import epub_namespaces
from benjaminhamon_document_manipulation_toolkit.xml import xpath_helpers


def create_xhtml() -> lxml.etree._ElementTree:
    namespaces = {
        None: epub_namespaces.xhtml_default_namespace,
        "epub": epub_namespaces.xhtml_epub_namespace,
    }

    html_element = lxml.etree.Element(lxml.etree.QName(epub_namespaces.xhtml_default_namespace, "html"), attrib = None, nsmap = namespaces) # type: ignore

    create_xhtml_subelement(html_element, "head")
    create_xhtml_subelement(html_element, "body")

    return lxml.etree.ElementTree(html_element)


def load_xhtml(xhtml_file_path: str) -> lxml.etree._ElementTree:
    xml_parser = lxml.html.XHTMLParser(encoding = "utf-8", remove_blank_text = True)
    xhtml_document = lxml.etree.parse(xhtml_file_path, xml_parser)

    body_as_xml = find_xhtml_element(xhtml_document.getroot(), "./x:body")
    body_as_xml.text = None

    return xhtml_document


def create_xhtml_subelement(
        parent: lxml.etree._Element, tag: str,
        attributes: Optional[dict] = None, text: Optional[str] = None) -> lxml.etree._Element:

    element = lxml.etree.SubElement(parent, lxml.etree.QName(epub_namespaces.xhtml_default_namespace, tag), attrib = attributes, nsmap = None)
    element.text = text

    return element


def try_find_xhtml_element_collection(element: lxml.etree._Element, xpath: str) -> List[lxml.etree._Element]:

    # XPath cannot work with the default namespace, thus we pass an explicit namespace for XHTML
    namespaces: Dict[Optional[str],str] = { "x": epub_namespaces.xhtml_default_namespace }

    return xpath_helpers.try_find_xml_element_collection(element, xpath, namespaces)


def try_find_xhtml_element(element: lxml.etree._Element, xpath: str) -> Optional[lxml.etree._Element]:

    # XPath cannot work with the default namespace, thus we pass an explicit namespace for XHTML
    namespaces: Dict[Optional[str],str] = { "x": epub_namespaces.xhtml_default_namespace }

    return xpath_helpers.try_find_xml_element(element, xpath, namespaces)


def find_xhtml_element(element: lxml.etree._Element, xpath: str) -> lxml.etree._Element:

    # XPath cannot work with the default namespace, thus we pass an explicit namespace for XHTML
    namespaces: Dict[Optional[str],str] = { "x": epub_namespaces.xhtml_default_namespace }

    return xpath_helpers.find_xml_element(element, xpath, namespaces)


def get_xhtml_title(document: lxml.etree._ElementTree) -> str:
    root = document.getroot()

    title_element = find_xhtml_element(root, "./x:head/x:title")
    if title_element.text is None:
        raise ValueError("Title element has no text")

    return title_element.text


def get_media_type(file_path: str) -> str:
    if file_path.endswith(".css"):
        return "text/css"
    if file_path.endswith(".jpeg"):
        return "image/jpeg"
    if file_path.endswith(".svg"):
        return "image/svg+xml"
    if file_path.endswith(".xhtml"):
        return "application/xhtml+xml"

    raise ValueError("Unsupported file type: '%s'" % file_path)
