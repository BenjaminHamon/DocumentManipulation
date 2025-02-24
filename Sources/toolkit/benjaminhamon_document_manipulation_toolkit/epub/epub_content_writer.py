# cspell:words idref itemref lxml nsmap oebps rootfile rootfiles

import datetime
import logging
import os
import urllib.parse
from typing import Any, List

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.epub import epub_namespaces
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation import EpubNavigation
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_xhtml_builder import EpubNavigationXhtmlBuilder
from benjaminhamon_document_manipulation_toolkit.epub.epub_package_document import EpubPackageDocument


logger = logging.getLogger("EpubContentWriter")


class EpubContentWriter:


    def __init__(self) -> None:
        self.encoding = "utf-8"
        self.pretty_print = True
        self.version = "3.0"


    def write_package_document_file(self,
            package_document_file_path: str, package_document: EpubPackageDocument, reference_base: str, simulate: bool = False) -> None:

        package_document_as_xhtml = self.convert_package_document_to_xhtml(package_document, reference_base)
        self.write_xml_file(package_document_file_path, package_document_as_xhtml, simulate = simulate)


    def write_navigation_file(self, toc_file_path: str, navigation: EpubNavigation, reference_base: str, simulate: bool = False) -> None:
        xhtml_builder = EpubNavigationXhtmlBuilder("Table of Contents")
        xhtml_builder.add_table_of_contents(navigation.navigation_items, reference_base)
        xhtml_builder.add_landmarks(navigation.landmarks, reference_base)

        navigation_document = xhtml_builder.get_xhtml_document()

        self.write_xml_file(toc_file_path, navigation_document, simulate = simulate)


    def write_container_file(self, container_file_path: str, package_document_file_path: str, simulate: bool = False) -> None:
        container_as_xml = self.create_container_as_xml(package_document_file_path)
        self.write_xml_file(container_file_path, container_as_xml, simulate = simulate)


    def write_xml_file(self, output_file_path: str, document_as_html: lxml.etree._ElementTree, simulate: bool = False) -> None:
        logger.debug("Writing '%s'", output_file_path)

        write_options = {
            "encoding": self.encoding,
            "pretty_print": self.pretty_print,
            "doctype": "<?xml version=\"1.0\" encoding=\"%s\"?>" % self.encoding,
        }

        document_as_xml_string: str = lxml.etree.tostring(document_as_html, **write_options).decode(self.encoding)

        if not simulate:
            with open(output_file_path + ".tmp", mode = "w", encoding = self.encoding) as output_file:
                output_file.write(document_as_xml_string)
            os.replace(output_file_path + ".tmp", output_file_path)


    def create_container_as_xml(self, opf_file_path: str) -> lxml.etree._ElementTree:
        namespaces = {
            None: epub_namespaces.container_namespace,
        }

        container_element = lxml.etree.Element(
            lxml.etree.QName(epub_namespaces.container_namespace, "container"), nsmap = namespaces, version = "1.0") # type: ignore

        root_file_collection_element = lxml.etree.SubElement(container_element, lxml.etree.QName(epub_namespaces.container_namespace, "rootfiles"))

        root_file_attributes = { "full-path": os.path.normpath(opf_file_path).replace("\\", "/"), "media-type": "application/oebps-package+xml" }
        lxml.etree.SubElement(root_file_collection_element, lxml.etree.QName(epub_namespaces.container_namespace, "rootfile"), attrib = root_file_attributes)

        return lxml.etree.ElementTree(container_element)


    def convert_package_document_to_xhtml(self, package_document: EpubPackageDocument, reference_base: str) -> lxml.etree._ElementTree:
        namespaces = {
            None: epub_namespaces.opf_default_namespace,
        }

        package_as_xhtml = lxml.etree.Element("package", nsmap = namespaces, version = self.version) # type: ignore
        package_as_xhtml.append(self.convert_package_document_metadata_to_xhtml(package_document.get_metadata_items()))

        identifier_item = package_document.get_identifier()
        if identifier_item is not None and identifier_item.xhtml_identifier is not None:
            package_as_xhtml.attrib["unique-identifier"] = identifier_item.xhtml_identifier

        manifest_as_xhtml = lxml.etree.SubElement(package_as_xhtml, "manifest")
        for manifest_item in package_document.get_manifest_items():
            reference_relative = os.path.relpath(manifest_item.reference, reference_base).replace("\\", "/")

            attributes = {
                "id": manifest_item.identifier,
                "href": urllib.parse.quote(reference_relative),
                "media-type": manifest_item.media_type,
            }

            if len(manifest_item.properties) > 0:
                attributes["properties"] = " ".join(manifest_item.properties)

            lxml.etree.SubElement(manifest_as_xhtml, "item", attributes)

        spine_as_xhtml = lxml.etree.SubElement(package_as_xhtml, "spine")
        for spine_item in package_document.get_spine_items():
            attributes = {
                "idref": spine_item.reference,
                "linear": "yes" if spine_item.is_linear else "no",
            }

            if len(spine_item.properties) > 0:
                attributes["properties"] = " ".join(spine_item.properties)

            lxml.etree.SubElement(spine_as_xhtml, "itemref", attributes)

        return lxml.etree.ElementTree(package_as_xhtml)


    def convert_package_document_metadata_to_xhtml(self, all_metadata_items: List[EpubMetadataItem]) -> lxml.etree._Element:

        def value_to_str(value: Any) -> str:
            if isinstance(value, str):
                return value
            if isinstance(value, int):
                return str(value)
            if isinstance(value, datetime.datetime):
                return value.replace(tzinfo = None).isoformat() + "Z"

            raise ValueError("Unsupported metadata value type: '%s'" % type(value))

        namespaces = {
            "dc": epub_namespaces.opf_dublin_core_namespace,
        }

        metadata_as_xhtml = lxml.etree.Element("metadata", nsmap = namespaces)

        for metadata_item in all_metadata_items:
            if metadata_item.is_meta:
                entry_as_xhtml = lxml.etree.SubElement(metadata_as_xhtml, "meta", property = metadata_item.key)
                entry_as_xhtml.text = value_to_str(metadata_item.value)

            else:
                namespace_key, metadata_key = metadata_item.key.split(":")
                tag = lxml.etree.QName(namespaces[namespace_key], metadata_key)
                entry_as_xhtml = lxml.etree.SubElement(metadata_as_xhtml, tag)
                entry_as_xhtml.text = value_to_str(metadata_item.value)

            if metadata_item.xhtml_identifier is not None:
                entry_as_xhtml.attrib["id"] = metadata_item.xhtml_identifier

            if metadata_item.refines is not None:
                for refine in metadata_item.refines:
                    if metadata_item.xhtml_identifier is None:
                        raise ValueError("Metadata refine must target an item with a XHTML identifier")

                    attributes = {
                        "refines": "#" + metadata_item.xhtml_identifier,
                        "property": refine.property,
                    }

                    if refine.scheme is not None:
                        attributes["scheme"] = refine.scheme

                    refine_as_xhtml = lxml.etree.SubElement(metadata_as_xhtml, "meta", attrib = attributes)
                    refine_as_xhtml.text = value_to_str(refine.value)

        return metadata_as_xhtml
