# pylint:disable = line-too-long

from typing import Any

from benjaminhamon_document_manipulation_toolkit.conversion.odt_to_xhtml_configuration import OdtToXhtmlConfiguration
from benjaminhamon_document_manipulation_toolkit.serialization.path_serialization_converter import PathSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "OdtToXhtmlConfigurationSerializationConverter":
    return OdtToXhtmlConfigurationSerializationConverter(PathSerializationConverter())


class OdtToXhtmlConfigurationSerializationConverter(SerializationConverter):


    def __init__(self, path_converter: SerializationConverter) -> None:
        self._path_converter = path_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        odt_to_xhtml_configuration = OdtToXhtmlConfiguration()

        # Document information
        odt_to_xhtml_configuration.revision_control = obj_as_serializable.get("revision_control", None)
        odt_to_xhtml_configuration.extra_metadata = obj_as_serializable.get("extra_metadata", None)

        # Content conversion
        odt_to_xhtml_configuration.xhtml_information_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("xhtml_information_template_file_path", None))
        odt_to_xhtml_configuration.xhtml_section_template_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("xhtml_section_template_file_path", None))
        odt_to_xhtml_configuration.style_sheet_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("style_sheet_file_path", None))
        odt_to_xhtml_configuration.style_map_file_path = self._path_converter.convert_from_serializable(obj_as_serializable.get("style_map_file_path", None))

        return odt_to_xhtml_configuration


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, OdtToXhtmlConfiguration):
            raise ValueError("obj is not of the expected type")

        return {
            "revision_control": obj.revision_control,
            "extra_metadata": obj.extra_metadata,
            "xhtml_information_template_file_path": obj.xhtml_information_template_file_path,
            "xhtml_section_template_file_path": obj.xhtml_section_template_file_path,
            "style_sheet_file_path": obj.style_sheet_file_path,
            "style_map_file_path": obj.style_map_file_path,
        }
