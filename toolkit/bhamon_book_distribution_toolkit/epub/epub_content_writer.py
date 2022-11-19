import glob
import os
from typing import List

import lxml.etree

from bhamon_book_distribution_toolkit.epub.epub_manifest import EpubManifest


class EpubContentWriter:

	
	def __init__(self) -> None:
		self.pretty_print = True
		self.encoding = "utf-8"
		self.version = "3.0"


	def write_mimetype_file(self, mimetype_file_path: str) -> None:
		with open(mimetype_file_path, mode = "w", encoding = self.encoding) as mimetype_file:
			mimetype_file.write("application/epub+zip")


	def write_opf_file(self, odf_file_path: str, package_document_definition:  lxml.etree.ElementTree) -> None:
		package_document_definition.write(odf_file_path, xml_declaration = True, pretty_print = self.pretty_print, encoding = self.encoding)


	def create_package_document_definition_as_xml(self, metadata: dict, manifest: EpubManifest) -> lxml.etree.ElementTree:
		namespaces = {
			None: "http://www.idpf.org/2007/opf",
		}

		package_as_xml = lxml.etree.Element("package", nsmap = namespaces, version = self.version)

		metadata_as_xml = lxml.etree.SubElement(package_as_xml, "metadata") # FIXME

		manifest_as_xml = lxml.etree.SubElement(package_as_xml, "manifest")
		for manifest_item in manifest.get_item_collection():
			attributes = {
				"href": manifest_item.path_relative_to_opf,
				"id": manifest_item.identifier,
				"media-type": manifest_item.media_type,
			}

			lxml.etree.SubElement(manifest_as_xml, "item", attributes)

		spine_as_xml = lxml.etree.SubElement(package_as_xml, "spine")
		for manifest_item in manifest.get_spine():
			lxml.etree.SubElement(spine_as_xml, "itemref", idref = manifest_item)

		return lxml.etree.ElementTree(package_as_xml)


	def create_manifest(self, content_directory: str) -> List[dict]:
		manifest = []

		all_file_entries = glob.glob(os.path.join(content_directory, "**"), recursive = True)
		for file_entry in all_file_entries:
			if os.path.isfile(file_entry):
				manifest.append({
					"href": os.path.relpath(file_entry, content_directory).replace("\\", "/"),
					"id": "FIXME",
					"media-type": self.get_media_type(file_entry),
				})

		return manifest


	def get_media_type(self, file_path: str) -> str:
		if file_path.endswith(".css"):
			return "text/css"
		if file_path.endswith(".xhtml"):
			return "application/xhtml+xml"
		if file_path.endswith(".ncx"):
			return "application/x-dtbncx+xml"

		raise ValueError("Unsupported file type: '%s'" % file_path)
