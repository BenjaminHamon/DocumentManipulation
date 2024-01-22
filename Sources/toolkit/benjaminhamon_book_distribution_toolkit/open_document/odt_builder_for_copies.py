# cspell:words addnext iterchildren localname lxml nsmap

import copy
from typing import Dict, List, Optional

import lxml.etree

from benjaminhamon_book_distribution_toolkit.open_document import odt_operations
from benjaminhamon_book_distribution_toolkit.xml import xml_operations


class OdtBuilderForCopies:
    """ Builder for an ODT document where we want to copy the same content several times """


    def __init__(self, xml_document_base: lxml.etree._ElementTree) -> None:
        self._xml_document = xml_document_base


    def get_xml_document(self) -> lxml.etree._ElementTree:
        return self._xml_document


    def add_copies(self, source_odt_document: lxml.etree._ElementTree, all_format_parameters: List[dict]) -> None:
        new_body = odt_operations.get_body_text_element(self._xml_document)
        source_body = odt_operations.get_body_text_element(source_odt_document)

        for item_index, format_parameters in enumerate(all_format_parameters):
            item_elements = self._copy_body_children(source_body, item_index, format_parameters, source_body.nsmap)

            for element in item_elements:
                self._append_element_to_body(new_body, element)


    def _copy_body_children(self,
            body_as_xml: lxml.etree._Element,
            item_index: int,
            format_parameters: Dict[str,str],
            namespaces: Dict[Optional[str], str],
            ) -> List[lxml.etree._Element]:

        element_collection: List[lxml.etree._Element] = []

        for element in body_as_xml.iterchildren():
            element_copy = copy.deepcopy(element)

            tag = lxml.etree.QName(element_copy).localname

            if tag not in ( "h", "p", "frame" ):
                raise ValueError("Unsupported text tag: '%s'" % tag)

            if tag == "frame":
                name_attribute_key = lxml.etree.QName(namespaces["draw"], "name")
                frame_name = element_copy.attrib.get(str(name_attribute_key))
                if frame_name is not None:
                    element_copy.attrib[str(name_attribute_key)] = str(frame_name) + "-" + str(item_index + 1)

                anchor_page_number_attribute_key = lxml.etree.QName(namespaces["text"], "anchor-page-number")
                anchor_page_number = element_copy.attrib.get(str(anchor_page_number_attribute_key))
                if anchor_page_number is not None:
                    element_copy.attrib[str(anchor_page_number_attribute_key)] = str(item_index + 1)

                element_collection.append(element_copy)

            if tag in ( "h", "p" ):
                xml_operations.format_text_in_xml(element_copy, format_parameters)
                element_collection.append(element_copy)

        return element_collection


    def _append_element_to_body(self, body: lxml.etree._Element, element: lxml.etree._Element):
        tag = lxml.etree.QName(element).localname

        if tag not in ( "h", "p", "frame" ):
            raise ValueError("Unsupported text tag: '%s'" % tag)

        if tag == "frame":
            last_frame = next((x for x in body.iterchildren(reversed = True) if lxml.etree.QName(x).localname == "frame"), None)
            if last_frame is None:
                body.append(element)
            else:
                last_frame.addnext(element)

        if tag in ( "h", "p" ):
            body.append(element)
