from typing import Any

from benjaminhamon_document_manipulation_toolkit.serialization.object_index import ObjectIndex
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


class SerializationConverterForComposition(SerializationConverter):


    def __init__(self, index: ObjectIndex, default_converter: SerializationConverter) -> None:
        self._index = index
        self._default_converter = default_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if isinstance(obj_as_serializable, str):
            if obj_as_serializable.startswith("$reference:"):
                key = obj_as_serializable[len("$reference:"):]
                if not self._index.contains_key(key):
                    raise KeyError("Reference not found in index: '%s'" % key)
                return self._index.get(key)

        return self._default_converter.convert_from_serializable(obj_as_serializable)


    def convert_to_serializable(self, obj: Any) -> Any:
        key = self._index.get_key(obj)
        if key is not None:
            return "$reference:" + key

        return self._default_converter.convert_to_serializable(obj)
