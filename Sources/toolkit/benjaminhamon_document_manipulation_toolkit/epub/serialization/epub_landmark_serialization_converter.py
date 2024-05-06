from typing import Any

from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "EpubLandmarkSerializationConverter":
    return EpubLandmarkSerializationConverter()


class EpubLandmarkSerializationConverter(SerializationConverter):


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        return EpubLandmark(
            epub_type = obj_as_serializable["type"],
            reference = obj_as_serializable["reference"],
            display_name = obj_as_serializable["display_name"])


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, EpubLandmark):
            raise ValueError("obj is not of the expected type")

        return {
            "type": obj.epub_type,
            "reference": obj.reference,
            "display_name": obj.display_name,
        }
