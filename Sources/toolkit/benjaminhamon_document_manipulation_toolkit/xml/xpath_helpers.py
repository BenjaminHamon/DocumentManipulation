# cspell:words lxml

from typing import Dict, List, Mapping, Optional

import lxml.etree


def try_find_xml_element_collection(
        element: lxml.etree._Element, xpath: str, namespaces: Optional[Mapping[str,str]] = None) -> List[lxml.etree._Element]:

    xpath_result = element.xpath(xpath, namespaces = namespaces)
    if xpath_result is None or not isinstance(xpath_result, list):
        return []

    return xpath_result # type: ignore


def try_find_xml_element(
        element: lxml.etree._Element, xpath: str, namespaces: Optional[Mapping[str,str]] = None) -> Optional[lxml.etree._Element]:

    xpath_result = element.xpath(xpath , namespaces = namespaces)
    if xpath_result is None or not isinstance(xpath_result, list) or len(xpath_result) == 0:
        return None

    return xpath_result[0] # type: ignore


def find_xml_element(
        element: lxml.etree._Element, xpath: str, namespaces: Optional[Mapping[str,str]] = None) -> lxml.etree._Element:

    result = try_find_xml_element(element, xpath, namespaces = namespaces)
    if result is None:
        raise ValueError("Element not found (XPath: '%s')" % xpath)

    return result


def sanitize_namespaces_for_xpath(namespaces: Mapping[Optional[str],str], default_namespace_prefix: Optional[str] = None) -> Dict[str, str]:
    if None in namespaces:
        if default_namespace_prefix is None:
            raise ValueError("Default namespace in present but no prefix was provided")
        namespaces_copy = { k: v for k, v in namespaces.items() if k is not None }
        namespaces_copy[default_namespace_prefix] = namespaces[None]
        return namespaces_copy

    return { k: v for k, v in namespaces.items() if k is not None }
