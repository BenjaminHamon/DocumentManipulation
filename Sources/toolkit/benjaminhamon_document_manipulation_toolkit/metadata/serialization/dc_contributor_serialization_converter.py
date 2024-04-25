from typing import Any

from benjaminhamon_document_manipulation_toolkit.metadata.dc_contributor import DcContributor
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "DcContributorSerializationConverter":
    return DcContributorSerializationConverter()


class DcContributorSerializationConverter(SerializationConverter):


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        return DcContributor(
            name = obj_as_serializable["name"],
            role = obj_as_serializable.get("role", None),
            file_as = obj_as_serializable.get("file_as", None),
        )


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, DcContributor):
            raise ValueError("obj is not of the expected type")

        return {
            "name": obj.name,
            "role": obj.role,
            "file_as": obj.file_as,
        }
