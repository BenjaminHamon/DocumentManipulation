import glob
import logging
import os
import shutil
import urllib.parse
import zipfile
from typing import Dict, List, Tuple

from benjaminhamon_document_manipulation_toolkit import text_operations
from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers
from benjaminhamon_document_manipulation_toolkit.epub.epub_content_writer import EpubContentWriter


logger = logging.getLogger("EpubPackageBuilder")


class EpubPackageBuilder:


    def __init__(self, content_writer: EpubContentWriter) -> None:
        self._content_writer = content_writer


    def stage_files(self, staging_directory: str, file_mappings: List[Tuple[str,str]], simulate: bool = False) -> None:
        logger.debug("Staging files")

        for source, destination in file_mappings:
            destination = os.path.normpath(os.path.join(staging_directory, destination))
            logger.debug("+ '%s' => '%s'", source, destination)

            if not simulate:
                os.makedirs(os.path.dirname(destination), exist_ok = True)
                shutil.copy(source, destination)


    def update_package_information(self,
            package_document_file_path: str, parameters: Dict[str,str], simulate: bool = False) -> None:

        logger.debug("Updating package information")

        with open(package_document_file_path, mode = "r", encoding = "utf-8") as package_document_file:
            package_document_text = package_document_file.read()

        package_document_text = text_operations.format_text(package_document_text, parameters)

        logger.debug("Writing '%s'", package_document_file_path)

        if not simulate:
            with open(package_document_file_path, mode = "w", encoding = "utf-8") as package_document_file:
                package_document_file.write(package_document_text)


    def update_xhtml_links(self,
            staging_directory: str, content_files: List[Tuple[str,str]], link_mappings: List[Tuple[str,str]], simulate: bool = False) -> None:

        logger.debug("Updating links")

        for source, destination in content_files:
            if source.endswith(".xhtml"):
                destination = os.path.join(staging_directory, destination)

                document = epub_xhtml_helpers.load_xhtml(destination)
                link_element_collection = epub_xhtml_helpers.try_find_xhtml_element_collection(document.getroot(), "./x:head/x:link")

                for link_element in link_element_collection:
                    link_value = str(link_element.attrib["href"])
                    link_components = urllib.parse.urlparse(link_value)

                    if link_components.scheme == "" and link_components.netloc == "": # Relative path
                        link_value_updated = os.path.normpath(os.path.join(os.path.dirname(source), link_value))
                        matching_mapping = next((x for x in link_mappings if os.path.normpath(x[0]) == link_value_updated), None)
                        if matching_mapping is not None:
                            link_value_updated = os.path.join(staging_directory, matching_mapping[1])
                        link_value_updated = os.path.relpath(link_value_updated, os.path.dirname(destination))
                        link_element.attrib["href"] = link_value_updated.replace("\\", "/")

                    else:
                        matching_mapping = next((x for x in link_mappings if x[0] == link_value), None)
                        if matching_mapping is not None:
                            link_element.attrib["href"] = matching_mapping[1]

                self._content_writer.write_xml_file(destination, document, simulate = simulate)


    def create_package(self, package_file_path: str, staging_directory: str, simulate: bool = False) -> None:
        logger.debug("Creating package (Path: '%s')", package_file_path)

        if not simulate:
            os.makedirs(os.path.dirname(package_file_path), exist_ok = True)

        all_file_entries = list(sorted(glob.glob(os.path.join(staging_directory, "**"), recursive = True)))

        logger.debug("Writing '%s'", package_file_path)

        if not simulate:
            with zipfile.ZipFile(package_file_path + ".tmp", mode = "w", compression = zipfile.ZIP_DEFLATED) as package_file:
                package_file.writestr("mimetype", "application/epub+zip", compress_type = zipfile.ZIP_STORED)

                for source in all_file_entries:
                    if os.path.isfile(source):
                        destination = os.path.normpath(os.path.relpath(source, staging_directory)).replace("\\", "/")
                        logger.debug("+ '%s' => '%s'", source, destination)
                        package_file.write(source, destination)

            os.replace(package_file_path + ".tmp", package_file_path)
