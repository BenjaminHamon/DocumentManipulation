import os
from typing import Any

from benjaminhamon_document_manipulation_toolkit.serialization.object_index import ObjectIndex
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer


class FileStructureSerializer:


    def __init__(self, object_serializer: Serializer, index: ObjectIndex, data_directory: str) -> None:
        self._object_serializer = object_serializer
        self._index = index
        self._data_directory = data_directory


    def add(self, key: str, obj: Any) -> None:
        self._index.add(self._sanitize_key(key), obj)


    def remove(self, key: str) -> None:
        self.remove(self._sanitize_key(key))


    def serialize(self, key: str) -> None:
        key = self._sanitize_key(key)
        path = self._get_data_file_path(key)
        os.makedirs(os.path.dirname(path), exist_ok = True)
        self._object_serializer.serialize_to_file(self._index.get(key), path)


    def deserialize(self, key: str, obj_type: type) -> Any:
        key = self._sanitize_key(key)
        path = self._get_data_file_path(key)
        return self._object_serializer.deserialize_from_file(path, obj_type)


    def _sanitize_key(self, key: str) -> str:
        return key.replace("\\", "/")


    def _get_data_file_path(self, key: str) -> str:
        return os.path.join(self._data_directory, os.path.normpath(key))
