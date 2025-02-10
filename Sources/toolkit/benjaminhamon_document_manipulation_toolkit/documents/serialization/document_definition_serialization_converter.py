from typing import Any

from benjaminhamon_document_manipulation_toolkit.documents.document_definition import DocumentDefinition
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "DocumentDefinitionSerializationConverter":
    return DocumentDefinitionSerializationConverter(PathSerializationConverter())


class DocumentDefinitionSerializationConverter(SerializationConverter):


    def __init__(self, path_converter: SerializationConverter) -> None:
        self._path_converter = path_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        front_section_file_paths = None
        if obj_as_serializable.get("front_section_file_paths") is not None:
            front_section_file_paths = [ self._path_converter.convert_from_serializable(x) for x in obj_as_serializable["front_section_file_paths"] ]

        content_section_file_paths = None
        if obj_as_serializable.get("content_section_file_paths") is not None:
            content_section_file_paths = [ self._path_converter.convert_from_serializable(x) for x in obj_as_serializable["content_section_file_paths"] ]

        back_section_file_paths = None
        if obj_as_serializable.get("back_section_file_paths") is not None:
            back_section_file_paths = [ self._path_converter.convert_from_serializable(x) for x in obj_as_serializable["back_section_file_paths"] ]

        return DocumentDefinition(
            information_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("information_file_path")),
            dc_metadata_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("dc_metadata_file_path")),
            extra_metadata = obj_as_serializable.get("extra_metadata"),
            source_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("source_file_path")),
            front_section_identifiers = obj_as_serializable.get("front_section_identifiers"),
            content_section_identifiers = obj_as_serializable.get("content_section_identifiers"),
            back_section_identifiers = obj_as_serializable.get("back_section_identifiers"),
            source_directory = self._path_converter.convert_from_serializable(obj_as_serializable.get("source_directory")),
            front_section_file_paths = front_section_file_paths,
            content_section_file_paths = content_section_file_paths,
            back_section_file_paths = back_section_file_paths,
        )


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, DocumentDefinition):
            raise ValueError("obj is not of the expected type")

        return {
            "information_file_path": self._path_converter.convert_to_serializable(obj.information_file_path),
            "dc_metadata_file_path": self._path_converter.convert_to_serializable(obj.dc_metadata_file_path),
            "extra_metadata": obj.extra_metadata,
            "source_file_path": self._path_converter.convert_to_serializable(obj.source_file_path),
            "front_section_identifiers": obj.front_section_identifiers,
            "content_section_identifiers": obj.content_section_identifiers,
            "back_section_identifiers": obj.back_section_identifiers,
            "front_section_file_paths": self._path_converter.convert_to_serializable(obj.front_section_file_paths),
            "content_section_file_paths": self._path_converter.convert_to_serializable(obj.content_section_file_paths),
            "back_section_file_paths": self._path_converter.convert_to_serializable(obj.back_section_file_paths),
        }
