# cspell:words localname lxml

from typing import Mapping

import lxml.etree

from benjaminhamon_document_manipulation_toolkit import text_operations


def format_text_in_xml(xml_root: lxml.etree._Element, format_parameters: Mapping[str,str]) -> None:
    for xml_element in xml_root.iter():
        tag = lxml.etree.QName(xml_element).localname
        if tag != "style" and xml_element.text is not None:
            xml_element.text = text_operations.format_text(xml_element.text, format_parameters)
