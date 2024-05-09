# cspell:words dateutil

import datetime
from typing import Any

import dateutil.parser

from benjaminhamon_document_manipulation_toolkit.serialization.serialization_converter import SerializationConverter


class DatetimeSerializationConverter(SerializationConverter):


    def convert_from_serializable(self, obj_as_serializable: Any) -> Any:
        if obj_as_serializable is None:
            return None

        if not isinstance(obj_as_serializable, str):
            raise ValueError("obj_as_serializable is not of the expected type")

        return dateutil.parser.parse(obj_as_serializable)


    def convert_to_serializable(self, obj: Any) -> Any:
        if obj is None:
            return None

        if isinstance(obj, datetime.datetime):
            raise ValueError("obj is not of the expected type")

        if obj.tzinfo == datetime.timezone.utc:
            return obj.replace(tzinfo = None).isoformat() + "Z"
        return obj.isoformat()
