from typing import Any

from benjaminhamon_document_manipulation_toolkit.epub.epub_generation_configuration import EpubGenerationConfiguration
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_landmark_serialization_converter
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_metadata_item_serialization_converter
from benjaminhamon_document_manipulation_toolkit.metadata.serialization import dc_metadata_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "EpubGenerationConfigurationSerializationConverter":
    return EpubGenerationConfigurationSerializationConverter(
        path_converter = PathSerializationConverter(),
        dc_metadata_converter = dc_metadata_serialization_converter.factory(),
        metadata_item_converter = epub_metadata_item_serialization_converter.factory(),
        landmark_converter = epub_landmark_serialization_converter.factory())


class EpubGenerationConfigurationSerializationConverter(SerializationConverter):


    def __init__(self,
            path_converter: SerializationConverter,
            dc_metadata_converter: SerializationConverter,
            metadata_item_converter: SerializationConverter,
            landmark_converter: SerializationConverter) -> None:

        self._path_converter = path_converter
        self._dc_metadata_converter = dc_metadata_converter
        self._metadata_item_converter = metadata_item_converter
        self._landmark_converter = landmark_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        epub_generation_configuration = EpubGenerationConfiguration()

        if obj_as_serializable.get("metadata", None) is not None:
            for metadata_item_as_serializable in obj_as_serializable["metadata"]:
                metadata_item = self._metadata_item_converter.convert_from_serializable(metadata_item_as_serializable)
                epub_generation_configuration.metadata.append(metadata_item)

        epub_generation_configuration.cover_file = self._path_converter.convert_from_serializable(obj_as_serializable.get("cover_file", None))

        for file_path in obj_as_serializable.get("content_files", []):
            epub_generation_configuration.content_files.append(self._path_converter.convert_from_serializable(file_path))

        for file_path in obj_as_serializable.get("resource_files", []):
            epub_generation_configuration.resource_files.append(self._path_converter.convert_from_serializable(file_path))

        epub_generation_configuration.link_overrides = obj_as_serializable.get("link_overrides", [])

        for landmark_as_serializable in obj_as_serializable.get("landmarks", []):
            landmark = self._landmark_converter.convert_from_serializable(landmark_as_serializable)
            epub_generation_configuration.landmarks.append(landmark)

        return epub_generation_configuration


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, EpubGenerationConfiguration):
            raise ValueError("obj is not of the expected type")

        metadata_as_serializable = [ self._metadata_item_converter.convert_to_serializable(x) for x in obj.metadata ]
        content_files_as_serializable = [ self._path_converter.convert_to_serializable(path) for path in obj.content_files ]
        resource_files_as_serializable = [ self._path_converter.convert_to_serializable(path) for path in obj.resource_files ]
        landmarks_as_serializable = [ self._landmark_converter.convert_to_serializable(x) for x in obj.landmarks ]

        return {
            "metadata": metadata_as_serializable,
            "cover_file": obj.cover_file,
            "content_files": content_files_as_serializable,
            "resource_files": resource_files_as_serializable,
            "link_overrides": list(obj.link_overrides),
            "landmarks": landmarks_as_serializable,
        }
