# cspell:words nsmap

from typing import List, Optional

import lxml.etree
import lxml.html


_epub_namespace = "http://www.idpf.org/2007/ops"
_xhtml_namespace = "http://www.w3.org/1999/xhtml"


def create_xhtml() -> lxml.etree._ElementTree:
    namespaces = {
        None: _xhtml_namespace,
        "epub": _epub_namespace,
    }

    html_element = lxml.etree.Element(lxml.etree.QName(_xhtml_namespace, "html"), attrib = None, nsmap = namespaces) # type: ignore

    create_xhtml_subelement(html_element, "head")
    create_xhtml_subelement(html_element, "body")

    return lxml.etree.ElementTree(html_element)


def load_xhtml(xhtml_file_path: str) -> lxml.etree._ElementTree:
    xml_parser = lxml.html.XHTMLParser(encoding = "utf-8", remove_blank_text = True)
    result = lxml.etree.parse(xhtml_file_path, xml_parser)
    return result


def create_xhtml_subelement(
        parent: lxml.etree._Element, tag: str,
        attributes: Optional[dict] = None, text: Optional[str] = None) -> lxml.etree._Element:

    element = lxml.etree.SubElement(parent, lxml.etree.QName(_xhtml_namespace, tag), attrib = attributes, nsmap = None)
    element.text = text

    return element


def try_find_xhtml_element_collection(element: lxml.etree._Element, xpath: str) -> List[lxml.etree._Element]:

    # XPath cannot work with the default namespace, thus we pass an explicit namespace for XHTML
    namespaces = { "x": _xhtml_namespace }

    xpath_result = element.xpath(xpath, namespaces = namespaces)
    if xpath_result is None or len(xpath_result) == 0: # type: ignore
        return []

    return xpath_result # type: ignore


def try_find_xhtml_element(element: lxml.etree._Element, xpath: str) -> Optional[lxml.etree._Element]:

    # XPath cannot work with the default namespace, thus we pass an explicit namespace for XHTML
    namespaces = { "x": _xhtml_namespace }

    xpath_result = element.xpath(xpath , namespaces = namespaces)
    if xpath_result is None or len(xpath_result) == 0: # type: ignore
        return None

    return xpath_result[0] # type: ignore


def find_xhtml_element(element: lxml.etree._Element, xpath: str) -> lxml.etree._Element:
    result = try_find_xhtml_element(element, xpath)
    if result is None:
        raise ValueError("Element not found (XPath: '%s')" % xpath)

    return result


def get_xhtml_title(document: lxml.etree._ElementTree) -> str:
    root = document.getroot()

    title_element = find_xhtml_element(root, "./x:head/x:title")
    if title_element.text is None:
        raise ValueError("Title element has no text")

    return title_element.text
