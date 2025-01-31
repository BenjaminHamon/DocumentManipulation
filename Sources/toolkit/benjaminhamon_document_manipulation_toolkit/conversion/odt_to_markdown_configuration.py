import dataclasses
from typing import Mapping, Optional


@dataclasses.dataclass()
class OdtToMarkdownConfiguration:

    # Document information
    extra_metadata: Optional[Mapping[str,str]] = None
    revision_control: Optional[str] = None

    # Content conversion
    style_map_file_path: Optional[str] = None
