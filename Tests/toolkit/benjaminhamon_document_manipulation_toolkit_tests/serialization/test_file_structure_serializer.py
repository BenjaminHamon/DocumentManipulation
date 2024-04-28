""" Unit tests for FileStructureSerializer """

import os
from typing import Any, List, Optional

import pytest

from benjaminhamon_document_manipulation_toolkit.serialization.object_index import ObjectIndex
from benjaminhamon_document_manipulation_toolkit.serialization.file_structure_serializer import FileStructureSerializer
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter_for_composition import SerializationConverterForComposition
from benjaminhamon_document_manipulation_toolkit.serialization.yaml_serializer import YamlSerializer


class _MyCollection:

    def __init__(self) -> None:
        self.identifier: Optional[str] = None
        self.all_items: List[_MyCollectionItem] = []


class _MyCollectionItem:

    def __init__(self, data: str) -> None:
        self.data = data


class _MyCollectionSerializationConverter(SerializationConverter):

    def __init__(self, item_converter: SerializationConverter) -> None:
        self._item_converter = item_converter

    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        collection = _MyCollection()
        collection.identifier = obj_as_serializable["identifier"]
        for item_as_serializable in obj_as_serializable["all_items"]:
            item = self._item_converter.convert_from_serializable(item_as_serializable)
            collection.all_items.append(item)
        return collection

    def convert_to_serializable(self, obj: Any) -> Any:
        if not isinstance(obj, _MyCollection):
            raise ValueError("obj is not of the expected type")

        all_items_as_serializable: List[Any] = []
        for item in obj.all_items:
            item_as_serializable = self._item_converter.convert_to_serializable(item)
            all_items_as_serializable.append(item_as_serializable)
        return { "identifier": obj.identifier, "all_items": all_items_as_serializable }


class _MyCollectionItemSerializationConverter(SerializationConverter):

    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")
        return _MyCollectionItem(obj_as_serializable["data"])

    def convert_to_serializable(self, obj: Any) -> Any:
        if not isinstance(obj, _MyCollectionItem):
            raise ValueError("obj is not of the expected type")
        return { "data": obj.data }


def test_serialize_with_references(tmpdir):
    index = ObjectIndex()
    data_directory = os.path.join(tmpdir, "Working")

    serializer = YamlSerializer()
    serializer.add_converter(_MyCollection,
        _MyCollectionSerializationConverter(SerializationConverterForComposition(index, _MyCollectionItemSerializationConverter())))

    file_structure_serializer = FileStructureSerializer(serializer, index, data_directory)

    collection = _MyCollection()
    collection.identifier = "collection"
    collection.all_items.append(_MyCollectionItem("first"))
    collection.all_items.append(_MyCollectionItem("second"))
    collection.all_items.append(_MyCollectionItem("third"))

    file_structure_serializer.add("Collection.yaml", collection)
    file_structure_serializer.add("ItemFirst.yaml", collection.all_items[0])
    file_structure_serializer.add("ItemSecond.yaml", collection.all_items[1])
    file_structure_serializer.add("ItemThird.yaml", collection.all_items[2])

    file_structure_serializer.serialize("Collection.yaml")

    assert os.path.exists(os.path.join(data_directory, "Collection.yaml"))
    assert not os.path.exists(os.path.join(data_directory, "ItemFirst.yaml"))
    assert not os.path.exists(os.path.join(data_directory, "ItemSecond.yaml"))
    assert not os.path.exists(os.path.join(data_directory, "ItemThird.yaml"))

    with open(os.path.join(data_directory, "Collection.yaml"), mode = "r", encoding = "utf-8") as data_file:
        collection_serialized = data_file.read()

    collection_serialized_expected = """
identifier: collection
all_items:
- $reference:ItemFirst.yaml
- $reference:ItemSecond.yaml
- $reference:ItemThird.yaml
"""

    collection_serialized_expected = collection_serialized_expected.lstrip()

    assert collection_serialized == collection_serialized_expected


def test_deserialize_with_references(tmpdir):
    index = ObjectIndex()
    data_directory = os.path.join(tmpdir, "Working")

    serializer = YamlSerializer()
    serializer.add_converter(_MyCollection,
        _MyCollectionSerializationConverter(SerializationConverterForComposition(index, _MyCollectionItemSerializationConverter())))

    file_structure_serializer = FileStructureSerializer(serializer, index, data_directory)

    collection = _MyCollection()
    collection.identifier = "collection"
    collection.all_items.append(_MyCollectionItem("first"))
    collection.all_items.append(_MyCollectionItem("second"))
    collection.all_items.append(_MyCollectionItem("third"))

    file_structure_serializer.add("Collection.yaml", collection)
    file_structure_serializer.add("ItemFirst.yaml", collection.all_items[0])
    file_structure_serializer.add("ItemSecond.yaml", collection.all_items[1])
    file_structure_serializer.add("ItemThird.yaml", collection.all_items[2])

    collection_serialized = """
identifier: collection
all_items:
- $reference:ItemFirst.yaml
- $reference:ItemSecond.yaml
- $reference:ItemThird.yaml
"""

    collection_serialized = collection_serialized.lstrip()

    os.makedirs(data_directory)
    with open(os.path.join(data_directory, "Collection.yaml"), mode = "w", encoding = "utf-8") as data_file:
        data_file.write(collection_serialized)

    collection_deserialized: _MyCollection = file_structure_serializer.deserialize("Collection.yaml", _MyCollection)

    assert collection_deserialized.identifier == collection.identifier
    assert collection_deserialized.all_items[0].data == collection.all_items[0].data
    assert collection_deserialized.all_items[1].data == collection.all_items[1].data
    assert collection_deserialized.all_items[2].data == collection.all_items[2].data


def test_deserialize_with_missing_references(tmpdir):
    index = ObjectIndex()
    data_directory = os.path.join(tmpdir, "Working")

    serializer = YamlSerializer()
    serializer.add_converter(_MyCollection,
        _MyCollectionSerializationConverter(SerializationConverterForComposition(index, _MyCollectionItemSerializationConverter())))

    file_structure_serializer = FileStructureSerializer(serializer, index, data_directory)

    collection = _MyCollection()
    collection.identifier = "collection"
    collection.all_items.append(_MyCollectionItem("first"))
    collection.all_items.append(_MyCollectionItem("second"))
    collection.all_items.append(_MyCollectionItem("third"))

    file_structure_serializer.add("Collection.yaml", collection)

    collection_serialized = """
identifier: collection
all_items:
- $reference:ItemFirst.yaml
- $reference:ItemSecond.yaml
- $reference:ItemThird.yaml
"""

    collection_serialized = collection_serialized.lstrip()

    os.makedirs(data_directory)
    with open(os.path.join(data_directory, "Collection.yaml"), mode = "w", encoding = "utf-8") as data_file:
        data_file.write(collection_serialized)

    with pytest.raises(KeyError):
        file_structure_serializer.deserialize("Collection.yaml", _MyCollection)
