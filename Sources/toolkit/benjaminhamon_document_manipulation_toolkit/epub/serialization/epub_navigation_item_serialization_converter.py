from typing import Any

from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_item import EpubNavigationItem
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "EpubNavigationItemSerializationConverter":
    return EpubNavigationItemSerializationConverter()


class EpubNavigationItemSerializationConverter(SerializationConverter):


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        return EpubNavigationItem(
            reference = obj_as_serializable["reference"],
            display_name = obj_as_serializable["display_name"],
        )


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, EpubNavigationItem):
            raise ValueError("obj is not of the expected type")

        return {
            "reference": obj.reference,
            "display_name": obj.display_name,
        }
