# cspell:words lxml

from typing import Dict, List, Optional

import lxml.etree


def try_find_xml_element_collection(
        element: lxml.etree._Element, xpath: str, namespaces: Optional[Dict[Optional[str],str]] = None) -> List[lxml.etree._Element]:

    xpath_result = element.xpath(xpath, namespaces = _sanitize_namespaces_for_xpath(namespaces))
    if xpath_result is None or not isinstance(xpath_result, list):
        return []

    return xpath_result # type: ignore


def try_find_xml_element(
        element: lxml.etree._Element, xpath: str, namespaces: Optional[Dict[Optional[str],str]] = None) -> Optional[lxml.etree._Element]:

    xpath_result = element.xpath(xpath , namespaces = _sanitize_namespaces_for_xpath(namespaces))
    if xpath_result is None or not isinstance(xpath_result, list) or len(xpath_result) == 0:
        return None

    return xpath_result[0] # type: ignore


def find_xml_element(
        element: lxml.etree._Element, xpath: str, namespaces: Optional[Dict[Optional[str],str]] = None) -> lxml.etree._Element:

    result = try_find_xml_element(element, xpath, namespaces = namespaces)
    if result is None:
        raise ValueError("Element not found (XPath: '%s')" % xpath)

    return result


def _sanitize_namespaces_for_xpath(namespaces: Optional[Dict[Optional[str],str]]) -> Optional[Dict[str, str]]:
    if namespaces is None:
        return None

    return { k: v for k, v in namespaces.items() if k is not None }
