import glob
import logging
import os
import shutil
import zipfile
from typing import Dict, List, Tuple

import yaml

from benjaminhamon_document_manipulation_toolkit import text_operations
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter


logger = logging.getLogger("EpubBuilder")


class EpubPackageBuilder:


    def __init__(self, content_writer: EpubContentWriter) -> None:
        self._content_writer = content_writer


    def load_file_mappings(self, configuration_directory: str) -> List[Tuple[str,str]]:
        file_mapping_collection: List[Tuple[str,str]] = []

        file_mapping_collection.append((os.path.join(configuration_directory, "content.opf"), os.path.join("EPUB", "content.opf")))
        file_mapping_collection.append((os.path.join(configuration_directory, "toc.xhtml"), os.path.join("EPUB", "toc.xhtml")))
        file_mapping_collection.append((os.path.join(configuration_directory, "container.xml"), os.path.join("META-INF", "container.xml")))

        file_mapping_listing_file_path = os.path.join(configuration_directory, "FileMappings.yaml")
        with open(file_mapping_listing_file_path, mode = "r", encoding = "utf-8") as file_mapping_listing_file:
            content_file_mappings: List[Dict[str,str]] = yaml.safe_load(file_mapping_listing_file)

        for file_mapping in content_file_mappings:
            file_mapping_collection.append((os.path.normpath(file_mapping["source"]), os.path.join("EPUB", os.path.normpath(file_mapping["destination"]))))

        return file_mapping_collection


    def stage_files(self, staging_directory: str, file_mappings: List[Tuple[str,str]], simulate: bool = False) -> None:
        logger.info("Staging files")

        for source, destination in file_mappings:
            destination = os.path.normpath(os.path.join(staging_directory, destination))
            logger.debug("+ '%s' => '%s'", source, destination)

            if not simulate:
                os.makedirs(os.path.dirname(destination), exist_ok = True)
                shutil.copy(source, destination)


    def update_package_information(self,
            package_document_file_path: str, parameters: Dict[str,str], simulate: bool = False) -> None:

        logger.info("Updating package information")

        with open(package_document_file_path, mode = "r", encoding = "utf-8") as package_document_file:
            package_document_text = package_document_file.read()

        package_document_text = text_operations.format_text(package_document_text, parameters)

        logger.debug("Writing '%s'", package_document_file_path)

        if not simulate:
            with open(package_document_file_path, mode = "w", encoding = "utf-8") as package_document_file:
                package_document_file.write(package_document_text)


    def update_xhtml_links(self,
            staging_directory: str, content_files: List[Tuple[str,str]], resource_links: List[Tuple[str,str]], simulate: bool = False) -> None:

        logger.info("Updating links")

        for source, destination in content_files:
            if source.endswith(".xhtml"):
                destination = os.path.join(staging_directory, destination)

                document = epub_xhtml_helpers.load_xhtml(destination)
                link_element_collection = epub_xhtml_helpers.try_find_xhtml_element_collection(document.getroot(), "./x:head/x:link")

                for link_element in link_element_collection:
                    link_raw_value = str(link_element.attrib["href"])
                    if link_raw_value.startswith("."):
                        link = os.path.normpath(os.path.join(os.path.dirname(source), link_raw_value))

                        matching_mapping = next((x for x in resource_links if os.path.normpath(x[0]) == link), None)
                        if matching_mapping is None:
                            raise ValueError("Link target not found: '%s'" % link_raw_value)

                        link_updated = os.path.join(staging_directory, matching_mapping[1])
                        link_updated = os.path.relpath(link_updated, os.path.dirname(destination))

                        link_element.attrib["href"] = link_updated.replace("\\", "/")

                self._content_writer.write_xml(destination, document, simulate = simulate)


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
