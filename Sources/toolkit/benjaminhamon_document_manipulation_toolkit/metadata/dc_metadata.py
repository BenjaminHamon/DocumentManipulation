# See https://www.dublincore.org/specifications/dublin-core/usageguide/elements/

import dataclasses
import datetime
from typing import List, Optional

from benjaminhamon_document_manipulation_toolkit.metadata.dc_contributor import DcContributor


@dataclasses.dataclass(frozen = True)
class DcMetadata: # pylint: disable = too-many-instance-attributes
    """ Document information based on the Dublin Core specifications """

    titles: Optional[List[str]] = None
    subjects: Optional[List[str]] = None
    descriptions: Optional[List[str]] = None
    document_types: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    creators: Optional[List[DcContributor]] = None
    publishers: Optional[List[str]] = None
    contributors: Optional[List[DcContributor]] = None
    rights: Optional[List[str]] = None
    dates: Optional[List[datetime.datetime]] = None
    document_formats: Optional[List[str]] = None
    identifiers: Optional[List[str]] = None
    languages: Optional[List[str]] = None
