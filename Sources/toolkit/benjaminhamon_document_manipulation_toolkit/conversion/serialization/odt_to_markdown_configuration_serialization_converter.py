# pylint:disable = line-too-long

from typing import Any

from benjaminhamon_document_manipulation_toolkit.conversion.odt_to_markdown_configuration import OdtToMarkdownConfiguration
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "OdtToMarkdownConfigurationSerializationConverter":
    return OdtToMarkdownConfigurationSerializationConverter(PathSerializationConverter())


class OdtToMarkdownConfigurationSerializationConverter(SerializationConverter):


    def __init__(self, path_converter: SerializationConverter) -> None:
        self._path_converter = path_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        odt_to_markdown_configuration = OdtToMarkdownConfiguration()

        # Document information
        odt_to_markdown_configuration.extra_metadata = obj_as_serializable.get("extra_metadata", None)
        odt_to_markdown_configuration.revision_control = obj_as_serializable.get("revision_control", None)

        # Content conversion
        odt_to_markdown_configuration.style_map_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("style_map_file_path", None))

        return odt_to_markdown_configuration


    def convert_to_serializable(self, obj: Any) -> Any:
        raise NotImplementedError
