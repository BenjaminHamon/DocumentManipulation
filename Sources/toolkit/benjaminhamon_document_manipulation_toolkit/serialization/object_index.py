from typing import Any, List, Optional, Set, Tuple


class ObjectIndex:


    def __init__(self) -> None:
        self._item_collection: List[Tuple[str,Optional[Any]]] = []
        self._key_index: Set[str] = set()


    def add(self, key: str, obj: Optional[Any]) -> None:
        if key in self._key_index:
            raise KeyError("Key already exists: '%s'" % key)

        self._key_index.add(key)
        self._item_collection.append((key, obj))


    def remove(self, key: str) -> None:
        if key not in self._key_index:
            raise KeyError("Key does not exist: '%s'" % key)

        obj_tuple = next(x for x in self._item_collection if x[0] == key)
        self._item_collection.remove(obj_tuple)
        self._key_index.remove(key)


    def get(self, key: str) -> Optional[Any]:
        return next((x[1] for x in self._item_collection if x[0] == key), None)


    def get_key(self, obj: Any) -> Optional[str]:
        return next((x[0] for x in self._item_collection if x[1] == obj), None)


    def contains(self, obj: Any) -> bool:
        return next((x for x in self._item_collection if x[1] == obj), None) is not None


    def contains_key(self, key: str) -> bool:
        return next((x for x in self._item_collection if x[0] == key), None) is not None
