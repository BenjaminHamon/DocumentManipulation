from typing import Any

from benjaminhamon_document_manipulation_toolkit.documents.document_information import DocumentInformation
from benjaminhamon_document_manipulation_toolkit.serialization.datetime_serialization_converter import DatetimeSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "DocumentInformationSerializationConverter":
    return DocumentInformationSerializationConverter(DatetimeSerializationConverter())


class DocumentInformationSerializationConverter(SerializationConverter):


    def __init__(self, datetime_converter: SerializationConverter) -> None:
        self._datetime_converter = datetime_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        return DocumentInformation(
            identifier = obj_as_serializable.get("identifier", None),
            language = obj_as_serializable.get("language", None),
            title = obj_as_serializable.get("title", None),
            author = obj_as_serializable.get("author", None),
            publisher = obj_as_serializable.get("publisher", None),
            publication_date = self._datetime_converter.convert_from_serializable(obj_as_serializable.get("publication_date", None)),
            copyright = obj_as_serializable.get("copyright", None),
            version_identifier = obj_as_serializable.get("version_identifier", None),
            version_display_name = obj_as_serializable.get("version_display_name", None),
        )


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, DocumentInformation):
            raise ValueError("obj is not of the expected type")

        return {
            "identifier": obj.identifier,
            "language": obj.language,
            "title": obj.title,
            "author": obj.author,
            "publisher": obj.publisher,
            "publication_date": self._datetime_converter.convert_to_serializable(obj.publication_date),
            "copyright": obj.copyright,
            "version_identifier": obj.version_identifier,
            "version_display_name": obj.version_display_name,
        }
