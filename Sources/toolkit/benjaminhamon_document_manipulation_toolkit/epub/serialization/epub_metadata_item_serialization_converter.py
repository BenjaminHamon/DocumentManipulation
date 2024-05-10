from typing import Any, List, Optional

from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_refine import EpubMetadataRefine
from benjaminhamon_document_manipulation_toolkit.epub.serialization import epub_metadata_refine_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "EpubMetadataItemSerializationConverter":
    return EpubMetadataItemSerializationConverter(epub_metadata_refine_serialization_converter.factory())


class EpubMetadataItemSerializationConverter(SerializationConverter):


    def __init__(self, refine_converter: SerializationConverter) -> None:
        self._refine_converter = refine_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        refine_collection: Optional[List[EpubMetadataRefine]] = None
        if obj_as_serializable.get("refines", None) is not None:
            refine_collection = []
            for refine_as_serializable in obj_as_serializable["refines"]:
                refine_collection.append(self._refine_converter.convert_from_serializable(refine_as_serializable))

        return EpubMetadataItem(
            key = obj_as_serializable["key"],
            value = obj_as_serializable["value"],
            is_meta = obj_as_serializable.get("is_meta", False),
            xhtml_identifier = obj_as_serializable.get("xhtml_identifier", None),
            refines = refine_collection)


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, EpubMetadataItem):
            raise ValueError("obj is not of the expected type")

        refines_as_serializable = None
        if obj.refines is not None:
            refines_as_serializable = []
            for refine in obj.refines:
                refines_as_serializable.append(self._refine_converter.convert_to_serializable(refine))

        return {
            "key": obj.key,
            "value": obj.value,
            "is_meta": obj.is_meta,
            "xhtml_identifier": obj.xhtml_identifier,
            "refines": refines_as_serializable,
        }
