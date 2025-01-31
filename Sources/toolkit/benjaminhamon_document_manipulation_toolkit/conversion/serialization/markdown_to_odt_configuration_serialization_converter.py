# cspell:words fodt
# pylint:disable = line-too-long

from typing import Any

from benjaminhamon_document_manipulation_toolkit.conversion.markdown_to_odt_configuration import MarkdownToOdtConfiguration
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "MarkdownToOdtConfigurationSerializationConverter":
    return MarkdownToOdtConfigurationSerializationConverter(PathSerializationConverter())


class MarkdownToOdtConfigurationSerializationConverter(SerializationConverter):


    def __init__(self, path_converter: SerializationConverter) -> None:
        self._path_converter = path_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        markdown_to_odt_configuration = MarkdownToOdtConfiguration()

        # Content conversion
        markdown_to_odt_configuration.fodt_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("fodt_template_file_path", None))
        markdown_to_odt_configuration.style_map_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("style_map_file_path", None))

        return markdown_to_odt_configuration


    def convert_to_serializable(self, obj: Any) -> Any:
        raise NotImplementedError
