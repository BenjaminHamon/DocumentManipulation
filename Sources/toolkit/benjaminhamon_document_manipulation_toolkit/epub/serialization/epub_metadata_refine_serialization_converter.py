from typing import Any

from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_refine import EpubMetadataRefine
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "EpubMetadataRefineSerializationConverter":
    return EpubMetadataRefineSerializationConverter()


class EpubMetadataRefineSerializationConverter(SerializationConverter):


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        return EpubMetadataRefine(
            property = obj_as_serializable["property"],
            value = obj_as_serializable["value"],
            scheme = obj_as_serializable.get("scheme", None),
        )


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, EpubMetadataRefine):
            raise ValueError("obj is not of the expected type")

        return {
            "property": obj.property,
            "value": obj.value,
            "scheme": obj.scheme,
        }
