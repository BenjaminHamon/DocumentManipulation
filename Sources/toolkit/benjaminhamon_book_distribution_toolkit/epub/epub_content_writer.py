# cspell:words dcterms idref itemref nsmap oebps opendocument rootfile rootfiles

import datetime
import logging
import os
from typing import Any, List
import urllib.parse

import lxml.etree

from benjaminhamon_book_distribution_toolkit.epub import epub_namespaces
from benjaminhamon_book_distribution_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_book_distribution_toolkit.epub.epub_package_document import EpubPackageDocument


logger = logging.getLogger("EpubContentWriter")


class EpubContentWriter:


    def __init__(self) -> None:
        self.encoding = "utf-8"
        self.pretty_print = True
        self.version = "3.0"


    def write_container_file(self, xml_file_path: str, opf_file_path: str,  simulate: bool = False) -> None:
        container_as_xml = self.create_container_as_xml(opf_file_path)
        self.write_xml(xml_file_path, container_as_xml, simulate = simulate)


    def write_opf_file(self, opf_file_path: str, package_document: EpubPackageDocument, simulate: bool = False) -> None:
        package_document_as_xml = self.convert_package_document_to_xml(package_document)
        self.write_xml(opf_file_path, package_document_as_xml, simulate = simulate)


    def write_xml(self, xml_file_path: str, document: lxml.etree._ElementTree, simulate: bool = False) -> None:
        logger.debug("Writing '%s'", xml_file_path)

        write_options = {
            "encoding": self.encoding,
            "pretty_print": self.pretty_print,
            "xml_declaration": True,
        }

        if not simulate:
            document.write(xml_file_path + ".tmp", **write_options)
            os.replace(xml_file_path + ".tmp", xml_file_path)


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


    def convert_package_document_to_xml(self, package_document: EpubPackageDocument) -> lxml.etree._ElementTree:
        namespaces = {
            None: epub_namespaces.opf_default_namespace,
        }

        package_as_xml = lxml.etree.Element("package", nsmap = namespaces, version = self.version) # type: ignore
        package_as_xml.append(self.convert_package_document_metadata_to_xml(package_document.get_metadata_items()))

        identifier_item = package_document.get_identifier()
        if identifier_item is not None:
            if identifier_item.xhtml_identifier is None:
                raise ValueError("Metadata dc:identifier must have a XHTML identifier")
            package_as_xml.attrib["unique-identifier"] = identifier_item.xhtml_identifier

        manifest_as_xml = lxml.etree.SubElement(package_as_xml, "manifest")
        for manifest_item in package_document.get_manifest_items():
            attributes = {
                "id": manifest_item.identifier,
                "href": urllib.parse.quote(manifest_item.path_relative_to_opf.replace("\\", "/")),
                "media-type": manifest_item.media_type,
            }

            if len(manifest_item.properties) > 0:
                attributes["properties"] = " ".join(manifest_item.properties)

            lxml.etree.SubElement(manifest_as_xml, "item", attributes)

        spine_as_xml = lxml.etree.SubElement(package_as_xml, "spine")
        for spine_item in package_document.get_spine_items():
            attributes = {
                "idref": spine_item.reference,
                "linear": "yes" if spine_item.is_linear else "no",
            }

            if len(spine_item.properties) > 0:
                attributes["properties"] = " ".join(spine_item.properties)

            lxml.etree.SubElement(spine_as_xml, "itemref", attributes)

        return lxml.etree.ElementTree(package_as_xml)


    def convert_package_document_metadata_to_xml(self, all_metadata_items: List[EpubMetadataItem]) -> lxml.etree._Element:

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

        metadata_as_xml = lxml.etree.Element("metadata", nsmap = namespaces)

        for metadata_item in all_metadata_items:
            if metadata_item.is_meta:
                entry_as_xml = lxml.etree.SubElement(metadata_as_xml, "meta", property = metadata_item.key)
                entry_as_xml.text = value_to_str(metadata_item.value)

            else:
                namespace_key, metadata_key = metadata_item.key.split(":")
                tag = lxml.etree.QName(namespaces[namespace_key], metadata_key)
                entry_as_xml = lxml.etree.SubElement(metadata_as_xml, tag)
                entry_as_xml.text = value_to_str(metadata_item.value)

            if metadata_item.xhtml_identifier is not None:
                entry_as_xml.attrib["id"] = metadata_item.xhtml_identifier

            for refine in metadata_item.refine_collection:
                if metadata_item.xhtml_identifier is None:
                    raise ValueError("Metadata refine must target an item with a XHTML identifier")

                attributes = {
                    "refines": "#" + metadata_item.xhtml_identifier,
                    "property": refine.key,
                }

                if refine.scheme is not None:
                    attributes["scheme"] = refine.scheme

                refine_as_xml = lxml.etree.SubElement(metadata_as_xml, "meta", attrib = attributes)
                refine_as_xml.text = value_to_str(refine.value)

        return metadata_as_xml
