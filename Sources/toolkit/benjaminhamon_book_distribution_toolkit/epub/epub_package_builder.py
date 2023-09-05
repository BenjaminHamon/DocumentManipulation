import glob
import logging
import os
import shutil
import zipfile
from typing import List, Tuple

from benjaminhamon_book_distribution_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_book_distribution_toolkit.epub.epub_content_writer import EpubContentWriter
from benjaminhamon_book_distribution_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_book_distribution_toolkit.epub.epub_navigation_builder import EpubNavigationBuilder
from benjaminhamon_book_distribution_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_book_distribution_toolkit.epub.epub_package_configuration import EpubPackageConfiguration
from benjaminhamon_book_distribution_toolkit.epub.epub_package_document import EpubPackageDocument


logger = logging.getLogger("EpubBuilder")


class EpubPackageBuilder:


    def __init__(self, content_writer: EpubContentWriter) -> None:
        self._content_writer = content_writer


    def stage_package_files(self,
            staging_directory: str, configuration: EpubPackageConfiguration, simulate: bool = False) -> None:

        self.stage_content_files(staging_directory, configuration.content_file_mappings, simulate = simulate)

        if not simulate:
            self.update_xhtml_links(staging_directory, configuration.content_file_mappings, configuration.resource_link_mappings)

        self.stage_navigation(staging_directory, configuration.navigation_items, configuration.landmarks, simulate = simulate)
        self.stage_package_document(staging_directory, configuration.package_document, simulate = simulate)
        self.stage_container(staging_directory, simulate = simulate)


    def stage_content_files(self,
            staging_directory: str, file_mappings: List[Tuple[str,str]], simulate: bool = False):

        epub_directory = os.path.join(staging_directory, "EPUB")

        self._stage_files(epub_directory, file_mappings, simulate = simulate)


    def _stage_files(self, staging_directory: str, file_mappings: List[Tuple[str,str]], simulate: bool = False) -> None:
        if not simulate:
            os.makedirs(staging_directory, exist_ok = True)

        for source, destination in file_mappings:
            destination = os.path.normpath(os.path.join(staging_directory, destination))
            logger.debug("+ '%s' => '%s'", source, destination)

            if not simulate:
                os.makedirs(os.path.dirname(destination), exist_ok = True)
                shutil.copy(source, destination)


    def update_xhtml_links(self,
            staging_directory: str, content_files: List[Tuple[str,str]], resource_links: List[Tuple[str,str]], simulate: bool = False) -> None:

        epub_directory = os.path.join(staging_directory, "EPUB")

        for source, destination in content_files:
            if source.endswith(".xhtml"):
                destination = os.path.join(epub_directory, destination)

                document = epub_xhtml_helpers.load_xhtml(destination)
                link_element_collection = epub_xhtml_helpers.try_find_xhtml_element_collection(document.getroot(), "./x:head/x:link")

                for link_element in link_element_collection:
                    link_raw_value = str(link_element.attrib["href"])
                    if link_raw_value.startswith("."):
                        link = os.path.normpath(os.path.join(os.path.dirname(source), link_raw_value))

                        matching_mapping = next((x for x in resource_links if os.path.normpath(x[0]) == link), None)
                        if matching_mapping is None:
                            raise ValueError("Link target not found: '%s'" % link_raw_value)

                        link_updated = os.path.join(epub_directory, matching_mapping[1])
                        link_updated = os.path.relpath(link_updated, os.path.dirname(destination))

                        link_element.attrib["href"] = link_updated.replace("\\", "/")

                self._content_writer.write_xml(destination, document, simulate = simulate)


    def stage_navigation(self,
            staging_directory: str, item_collection: List[EpubNavigationItem], landmark_collection: List[EpubLandmark], simulate: bool = False) -> None:

        xhtml_file_path = os.path.join(staging_directory, "EPUB", "toc.xhtml")

        navigation_builder = EpubNavigationBuilder("Table of Contents")
        navigation_builder.add_table_of_contents(item_collection)
        navigation_builder.add_landmarks(landmark_collection)

        navigation_document = navigation_builder.get_xhtml_document()

        self._content_writer.write_xml(xhtml_file_path, navigation_document, simulate = simulate)


    def stage_package_document(self,
            staging_directory: str, package_document_definition: EpubPackageDocument, simulate: bool = False) -> None:

        opf_file_path = os.path.join(staging_directory, "EPUB", "package.opf")
        self._content_writer.write_opf_file(opf_file_path, package_document_definition, simulate = simulate)


    def stage_container(self, staging_directory: str, simulate: bool = False) -> None:
        container_xml_file_path = os.path.join(staging_directory, "META-INF", "container.xml")
        opf_file_path = os.path.join(staging_directory, "EPUB", "package.opf")

        if not simulate:
            os.makedirs(os.path.dirname(container_xml_file_path), exist_ok = True)
        self._content_writer.write_container_file(container_xml_file_path, opf_file_path, simulate = simulate)


    def create_package(self, package_file_path: str, staging_directory: str, simulate: bool = False) -> None:
        logger.info("Creating package (Path: '%s')", package_file_path)

        if not simulate:
            os.makedirs(os.path.dirname(package_file_path), exist_ok = True)

        all_file_entries = list(sorted(glob.glob(os.path.join(staging_directory, "**"), recursive = True)))

        if not simulate:
            with zipfile.ZipFile(package_file_path + ".tmp", mode = "w", compression = zipfile.ZIP_DEFLATED) as package_file:
                package_file.writestr("mimetype", "application/epub+zip", compress_type = zipfile.ZIP_STORED)

                for source in all_file_entries:
                    if os.path.isfile(source):
                        destination = os.path.normpath(os.path.relpath(source, staging_directory)).replace("\\", "/")
                        logger.debug("+ '%s' => '%s'", source, destination)
                        package_file.write(source, destination)

            os.replace(package_file_path + ".tmp", package_file_path)
