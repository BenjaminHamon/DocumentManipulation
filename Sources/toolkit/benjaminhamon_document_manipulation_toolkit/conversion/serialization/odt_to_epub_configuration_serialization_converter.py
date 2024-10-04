# cspell:words fodt
# pylint:disable = line-too-long

from typing import Any

from benjaminhamon_document_manipulation_toolkit.conversion.odt_to_epub_configuration import OdtToEpubConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_metadata_item_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_landmark_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "OdtToEpubConfigurationSerializationConverter":
    return OdtToEpubConfigurationSerializationConverter(
        metadata_item_converter = epub_metadata_item_serialization_converter.factory(),
        path_converter = PathSerializationConverter(),
        landmark_converter = epub_landmark_serialization_converter.factory())


class OdtToEpubConfigurationSerializationConverter(SerializationConverter):


    def __init__(self,
            metadata_item_converter: SerializationConverter,
            path_converter: SerializationConverter,
            landmark_converter: SerializationConverter) -> None:

        self._metadata_item_converter = metadata_item_converter
        self._path_converter = path_converter
        self._landmark_converter = landmark_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any: # pylint: disable = too-many-branches
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        odt_to_epub_configuration = OdtToEpubConfiguration()

        # Document information
        odt_to_epub_configuration.information_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("information_file_path", None))
        odt_to_epub_configuration.dc_metadata_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("dc_metadata_file_path", None))
        if obj_as_serializable.get("extra_metadata", None) is not None:
            odt_to_epub_configuration.extra_metadata = []
            for metadata_item_as_serializable in obj_as_serializable["extra_metadata"]:
                odt_to_epub_configuration.extra_metadata.append(self._metadata_item_converter.convert_from_serializable(metadata_item_as_serializable))
        odt_to_epub_configuration.revision_control = obj_as_serializable.get("revision_control", None)
        odt_to_epub_configuration.xhtml_information_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("xhtml_information_template_file_path", None))

        # Sources
        odt_to_epub_configuration.source_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("source_file_path", None))
        odt_to_epub_configuration.source_section_regex = obj_as_serializable.get("source_section_regex", None)
        odt_to_epub_configuration.fodt_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("fodt_template_file_path", None))
        odt_to_epub_configuration.cover_file = self._path_converter.convert_from_serializable(obj_as_serializable.get("cover_file", None))
        odt_to_epub_configuration.cover_svg_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("cover_svg_template_file_path", None))

        # Content conversion
        odt_to_epub_configuration.xhtml_section_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("xhtml_section_template_file_path", None))
        odt_to_epub_configuration.style_sheet_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("style_sheet_file_path", None))
        odt_to_epub_configuration.style_map_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("style_map_file_path", None))

        # Package
        if obj_as_serializable.get("content_files_before", None) is not None:
            for file_path in obj_as_serializable["content_files_before"]:
                odt_to_epub_configuration.content_files_before.append(self._path_converter.convert_from_serializable(file_path))
        if obj_as_serializable.get("content_files_after", None) is not None:
            for file_path in obj_as_serializable["content_files_after"]:
                odt_to_epub_configuration.content_files_after.append(self._path_converter.convert_from_serializable(file_path))
        if obj_as_serializable.get("resource_files", None) is not None:
            for file_path in obj_as_serializable["resource_files"]:
                odt_to_epub_configuration.resource_files.append(self._path_converter.convert_from_serializable(file_path))
        if obj_as_serializable.get("link_overrides", None) is not None:
            odt_to_epub_configuration.link_overrides = obj_as_serializable["link_overrides"]
        if obj_as_serializable.get("landmarks", None) is not None:
            for landmark_as_serializable in obj_as_serializable["landmarks"]:
                odt_to_epub_configuration.landmarks.append(self._landmark_converter.convert_from_serializable(landmark_as_serializable))

        return odt_to_epub_configuration


    def convert_to_serializable(self, obj: Any) -> Any:
        raise NotImplementedError
