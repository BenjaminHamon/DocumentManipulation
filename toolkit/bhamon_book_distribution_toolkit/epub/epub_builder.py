import glob
import logging
import os
import shutil
from typing import List, Tuple
import zipfile

from bhamon_book_distribution_toolkit import convert_helpers
from bhamon_book_distribution_toolkit.documents.heading_element import HeadingElement
from bhamon_book_distribution_toolkit.documents.root_element import RootElement
from bhamon_book_distribution_toolkit.epub.epub_content_writer import EpubContentWriter
from bhamon_book_distribution_toolkit.epub.epub_manifest import EpubManifest
from bhamon_book_distribution_toolkit.epub.epub_xhtml_writer import EpubXhtmlWriter


logger = logging.getLogger("Epub")


class EpubBuilder:


	def __init__(self, content_writer: EpubContentWriter, xhtml_writer: EpubXhtmlWriter) -> None:
		self._content_writer = content_writer
		self._xhtml_writer = xhtml_writer


	def stage_meta_information_files(self, staging_directory: str, file_collection: List[str], simulate: bool = False) -> None:
		container_entry = next((file_entry for file_entry in file_collection if os.path.basename(file_entry) == "container.xml"), None)
		if container_entry is None:
			raise ValueError("A file 'container.xml' is required")

		file_mappings = [ (file_entry, os.path.join("META-INF", os.path.basename(file_entry))) for file_entry in file_collection ]

		self._stage_files(staging_directory, file_mappings, simulate = simulate)


	def stage_epub_content_files(self, staging_directory: str, file_mappings: List[Tuple[str,str]], simulate: bool = False):
		epub_directory = os.path.join(staging_directory, "EPUB")

		self._stage_files(epub_directory, file_mappings, simulate = simulate)


	def stage_text_from_document(self, staging_directory: str, document_content: RootElement, all_stylesheet_links: List[str], simulate: bool = False) -> None:
		epub_content_directory = os.path.join(staging_directory, "EPUB", "Content")

		if not simulate:
			os.makedirs(epub_content_directory, exist_ok = True)

		section_count = sum(1 for _ in document_content.enumerate_sections())
		all_stylesheet_links = [ os.path.join("..", stylesheet).replace("\\", "/") for stylesheet in all_stylesheet_links ]

		for section_index, section in enumerate(document_content.enumerate_sections()):
			identifier = self._generate_section_file_name(section.get_heading(), section_index, section_count)
			xhtml_file_path = os.path.join(epub_content_directory, identifier + ".xhtml")

			logger.debug("Writing '%s'", xhtml_file_path)
			xhtml_content = self._xhtml_writer.create_xhtml_from_section(section, all_stylesheet_links)

			if not simulate:
				self._xhtml_writer.write_xhtml_file(xhtml_file_path, xhtml_content)


	def _generate_section_file_name(self, heading: HeadingElement, section_index: int, section_count: int) -> str:
		name_elements = []
		name_elements.append(str(section_index + 1).rjust(len(str(section_count)), "0"))

		if heading.category is not None:
			name_elements.append(heading.category)
			if heading.index_in_category is not None:
				name_elements[-1] += " " + str(heading.index_in_category)

		name_elements.append(heading.get_text().text)

		return convert_helpers.sanitize_for_file_name(" - ".join(name_elements))


	def _stage_files(self, staging_directory: str, file_mappings: List[Tuple[str,str]], simulate: bool = False) -> None:
		if not simulate:
			os.makedirs(staging_directory, exist_ok = True)

		for source, destination in file_mappings:
			destination = os.path.normpath(os.path.join(staging_directory, destination))
			logger.debug("+ '%s' => '%s'", source, destination)

			if not simulate:
				os.makedirs(os.path.dirname(destination), exist_ok = True)
				shutil.copy(source, destination)


	def create_package_document_definition(self, staging_directory: str, metadata: dict, manifest: EpubManifest, simulate: bool = False) -> None:
		opf_file_path = os.path.join(staging_directory, "EPUB", "content.opf")
		package_document_definition = self._content_writer.create_package_document_definition_as_xml(metadata, manifest)

		logger.debug("Writing '%s'", opf_file_path)

		if not simulate:
			self._content_writer.write_opf_file(opf_file_path, package_document_definition)


	def create_package(self, package_file_path: str, staging_directory: str, simulate: bool = False) -> None:
		logger.info("Creating package (Path: '%s')", package_file_path)

		if not simulate:
			os.makedirs(os.path.dirname(package_file_path), exist_ok = True)

		all_file_entries = glob.glob(os.path.join(staging_directory, "**"), recursive = True)

		if not simulate:
			with zipfile.ZipFile(package_file_path + ".tmp", mode = "w", compression = zipfile.ZIP_DEFLATED) as package_file:
				package_file.writestr("mimetype", "application/epub+zip", compress_type = zipfile.ZIP_STORED)

				for source in all_file_entries:
					if os.path.isfile(source):
						destination = os.path.normpath(os.path.relpath(source, staging_directory)).replace("\\", "/")
						logger.debug("+ '%s' => '%s'", source, destination)
						package_file.write(source, destination)

			os.replace(package_file_path + ".tmp", package_file_path)
