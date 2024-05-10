import datetime
from typing import Any, List, Optional

from benjaminhamon_document_manipulation_toolkit.metadata.dc_contributor import DcContributor
from benjaminhamon_document_manipulation_toolkit.metadata.dc_metadata import DcMetadata
from benjaminhamon_document_manipulation_toolkit.metadata.serialization import dc_contributor_serialization_converter
from benjaminhamon_document_manipulation_toolkit.serialization.datetime_serialization_converter import DatetimeSerializationConverter
from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


def factory() -> "DcMetadataSerializationConverter":
    return DcMetadataSerializationConverter(
        datetime_converter = DatetimeSerializationConverter(),
        contributor_converter = dc_contributor_serialization_converter.factory())


class DcMetadataSerializationConverter(SerializationConverter):


    def __init__(self, datetime_converter: SerializationConverter, contributor_converter: SerializationConverter) -> None:
        self._datetime_converter = datetime_converter
        self._contributor_converter = contributor_converter


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, dict):
            raise ValueError("obj_as_serializable is not of the expected type")

        creators: Optional[List[DcContributor]] = None
        if obj_as_serializable.get("creators", None) is not None:
            creators = []
            for creator_as_serializable in obj_as_serializable["creators"]:
                creators.append(self._contributor_converter.convert_from_serializable(creator_as_serializable))

        contributors: Optional[List[DcContributor]] = None
        if obj_as_serializable.get("contributors", None) is not None:
            contributors = []
            for contributor_as_serializable in obj_as_serializable["contributors"]:
                contributors.append(self._contributor_converter.convert_from_serializable(contributor_as_serializable))

        dates: Optional[List[datetime.datetime]] = None
        if obj_as_serializable.get("date", None) is not None:
            dates = []
            for date_as_serializable in obj_as_serializable["dates"]:
                dates.append(self._datetime_converter.convert_from_serializable(date_as_serializable).date())

        return DcMetadata(
            titles = obj_as_serializable.get("titles", None),
            subjects = obj_as_serializable.get("subjects", None),
            descriptions = obj_as_serializable.get("descriptions", None),
            document_types = obj_as_serializable.get("types", None),
            sources = obj_as_serializable.get("sources", None),
            creators = creators,
            publishers = obj_as_serializable.get("publishers", None),
            contributors = contributors,
            rights = obj_as_serializable.get("rights", None),
            dates = dates,
            document_formats = obj_as_serializable.get("formats", None),
            identifiers = obj_as_serializable.get("identifiers", None),
            languages = obj_as_serializable.get("languages", None),
        )


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if not isinstance(obj, DcMetadata):
            raise ValueError("obj is not of the expected type")

        creators_as_serializable: Optional[List[dict]] = None
        if obj.creators is not None:
            creators_as_serializable = []
            for contributor in obj.creators:
                creators_as_serializable.append(self._contributor_converter.convert_to_serializable(contributor))

        contributors_as_serializable: Optional[List[dict]] = None
        if obj.contributors is not None:
            contributors_as_serializable = []
            for contributor in obj.contributors:
                contributors_as_serializable.append(self._contributor_converter.convert_to_serializable(contributor))

        dates_as_serializable: Optional[List[str]] = None
        if obj.dates is not None:
            dates_as_serializable = []
            for date in obj.dates:
                dates_as_serializable.append(self._datetime_converter.convert_to_serializable(date))

        return {
            "titles": obj.titles,
            "subjects": obj.subjects,
            "descriptions": obj.descriptions,
            "types": obj.document_types,
            "sources": obj.sources,
            "creators": creators_as_serializable,
            "publishers": obj.publishers,
            "contributors": contributors_as_serializable,
            "rights": obj.rights,
            "dates": dates_as_serializable,
            "formats": obj.document_formats,
            "identifiers": obj.identifiers,
            "languages": obj.languages,
        }
