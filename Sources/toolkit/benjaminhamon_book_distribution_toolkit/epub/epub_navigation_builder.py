# cspell:words nsmap

from typing import List

import lxml.etree

from benjaminhamon_book_distribution_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_book_distribution_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_book_distribution_toolkit.epub.epub_navigation_item import EpubNavigationItem


class EpubNavigationBuilder:


    def __init__(self, title: str) -> None:
        self._xhtml_document = EpubNavigationBuilder._create_document(title)


    @staticmethod
    def _create_document(title: str) -> lxml.etree._ElementTree:
        document = epub_xhtml_helpers.create_xhtml()

        head_element = epub_xhtml_helpers.find_xhtml_element(document.getroot(), "./x:head")
        title_element = epub_xhtml_helpers.create_xhtml_subelement(head_element, "title")
        title_element.text = title

        return document


    def get_xhtml_document(self) -> lxml.etree._ElementTree:
        return self._xhtml_document


    def add_table_of_contents(self, item_collection: List[EpubNavigationItem]) -> None:
        body_element = epub_xhtml_helpers.find_xhtml_element(self._xhtml_document.getroot(), "./x:body")

        nav_element = epub_xhtml_helpers.create_xhtml_subelement(body_element, "nav",
            attributes = { lxml.etree.QName(body_element.nsmap["epub"], "type"): "toc" })

        epub_xhtml_helpers.create_xhtml_subelement(nav_element, "h1", text = "Table of Contents")

        list_element = epub_xhtml_helpers.create_xhtml_subelement(nav_element, "ol")

        for item in item_collection:
            list_item_element = epub_xhtml_helpers.create_xhtml_subelement(list_element, "li")
            epub_xhtml_helpers.create_xhtml_subelement(list_item_element, "a", attributes = { "href": item.reference }, text = item.display_name)


    def add_landmarks(self, item_collection: List[EpubLandmark]) -> None:
        body_element = epub_xhtml_helpers.find_xhtml_element(self._xhtml_document.getroot(), "./x:body")

        nav_element = epub_xhtml_helpers.create_xhtml_subelement(body_element, "nav",
            attributes = { lxml.etree.QName(body_element.nsmap["epub"], "type"): "landmarks" })

        epub_xhtml_helpers.create_xhtml_subelement(nav_element, "h1", text = "Landmarks")

        list_element = epub_xhtml_helpers.create_xhtml_subelement(nav_element, "ol")

        for item in item_collection:
            list_item_element = epub_xhtml_helpers.create_xhtml_subelement(list_element, "li")
            attributes = { lxml.etree.QName(body_element.nsmap["epub"], "type"): item.epub_type, "href": item.reference }
            epub_xhtml_helpers.create_xhtml_subelement(list_item_element, "a", attributes = attributes, text = item.display_name)
