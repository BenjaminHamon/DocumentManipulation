# cspell:words lxml

import os

import lxml.etree


def update_link(link_element: lxml.etree._Element, document_old_path: str, document_new_path: str) -> None:
    link_reference = str(link_element.attrib["href"])
    relative_to_cwd = os.path.join(os.path.dirname(document_old_path), link_reference)
    relative_to_new_path = os.path.normpath(os.path.relpath(relative_to_cwd, os.path.dirname(document_new_path)))
    link_element.attrib["href"] = relative_to_new_path.replace("\\", "/")


def add_style_sheet(html_element: lxml.etree._Element, tag: str, css_file_path: str, document_file_path: str) -> None:
    relative_css_file_path = os.path.relpath(css_file_path, os.path.dirname(document_file_path))
    attributes = { "href": relative_css_file_path.replace("\\", "/"), "rel": "stylesheet", "type": "text/css" }
    lxml.etree.SubElement(html_element, tag, attrib = attributes)
