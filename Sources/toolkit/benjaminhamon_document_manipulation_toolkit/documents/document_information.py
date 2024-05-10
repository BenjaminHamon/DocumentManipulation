import dataclasses
import datetime
from typing import Optional


@dataclasses.dataclass(frozen = True)
class DocumentInformation:
    identifier: Optional[str] = None
    language: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[datetime.datetime] = None
    copyright: Optional[str] = None
    version_identifier: Optional[str] = None
    version_display_name: Optional[str] = None
