import dataclasses
from typing import Mapping, Optional


@dataclasses.dataclass()
class OdtToXhtmlConfiguration:

    # Document information
    revision_control: Optional[str] = None
    extra_metadata: Optional[Mapping[str,str]] = None

    # Content conversion
    xhtml_information_template_file_path: Optional[str] = None
    xhtml_section_template_file_path: Optional[str] = None
    style_sheet_file_path: Optional[str] = None
    style_map_file_path: Optional[str] = None
