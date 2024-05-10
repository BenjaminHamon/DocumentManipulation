from typing import Any, List, Tuple

from benjaminhamon_document_manipulation_toolkit.epub.epub_content_configuration import EpubContentConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_landmark_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_navigation_item_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "EpubContentConfigurationSerializationConverter":
    return EpubContentConfigurationSerializationConverter(
        path_converter = PathSerializationConverter(),
        navigation_item_converter = epub_navigation_item_serialization_converter.factory(),
        landmark_converter = epub_landmark_serialization_converter.factory())


class EpubContentConfigurationSerializationConverter(SerializationConverter):


    def __init__(self,
            path_converter: SerializationConverter,
            navigation_item_converter: SerializationConverter,
            landmark_converter: SerializationConverter) -> None:

        self._path_converter = path_converter
        self._navigation_item_converter = navigation_item_converter
        self._landmark_converter = landmark_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        epub_content_configuration = EpubContentConfiguration()

        if obj_as_serializable.get("file_mappings", None) is not None:
            for file_mapping_as_serializable in obj_as_serializable["file_mappings"]:
                source = self._path_converter.convert_from_serializable(file_mapping_as_serializable[0])
                destination = self._path_converter.convert_from_serializable(file_mapping_as_serializable[1])
                epub_content_configuration.file_mappings.append((source, destination))

        if obj_as_serializable.get("link_mappings", None) is not None:
            for link_mapping_as_serializable in obj_as_serializable["link_mappings"]:
                source = self._path_converter.convert_from_serializable(link_mapping_as_serializable[0])
                destination = self._path_converter.convert_from_serializable(link_mapping_as_serializable[1])
                epub_content_configuration.link_mappings.append((source, destination))

        return epub_content_configuration


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, EpubContentConfiguration):
            raise ValueError("obj is not of the expected type")

        file_mappings_as_serializable: List[Tuple[str,str]] = []
        for file_mapping in obj.file_mappings:
            source = self._path_converter.convert_to_serializable(file_mapping[0])
            destination = self._path_converter.convert_to_serializable(file_mapping[1])
            file_mappings_as_serializable.append((source, destination))

        link_mappings_as_serializable: List[Tuple[str,str]] = []
        for link_mapping in obj.link_mappings:
            source = self._path_converter.convert_to_serializable(link_mapping[0])
            destination = self._path_converter.convert_to_serializable(link_mapping[1])
            link_mappings_as_serializable.append((source, destination))

        return {
            "file_mappings": file_mappings_as_serializable,
            "link_mappings": link_mappings_as_serializable,
        }
