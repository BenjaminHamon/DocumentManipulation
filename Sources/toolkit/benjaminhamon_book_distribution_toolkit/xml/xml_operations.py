# cspell:words lxml

from typing import Dict

import lxml.etree

from benjaminhamon_book_distribution_toolkit import text_operations


def format_text_in_xml(xml_root: lxml.etree._Element, format_parameters: Dict[str,str]) -> None:
    for xml_element in xml_root.iter():
        if xml_element.text is not None:
            xml_element.text = text_operations.format_text(xml_element.text, format_parameters)
