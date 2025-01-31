import dataclasses
from typing import List, Optional


@dataclasses.dataclass(frozen = True)
class DocumentDefinition: # pylint: disable = too-many-instance-attributes
    """Class describing a complete document by linking all its components"""

    # Information
    information_file_path: Optional[str] = None
    dc_metadata_file_path: Optional[str] = None
    extra_metadata: Optional[dict] = None

    # Content (single file)
    source_file_path: Optional[str] = None
    front_section_identifiers: Optional[List[str]] = None
    content_section_identifiers: Optional[List[str]] = None
    back_section_identifiers: Optional[List[str]] = None

    # Content (many files)
    source_directory: Optional[str] = None
    front_section_file_paths: Optional[List[str]] = None
    content_section_file_paths: Optional[List[str]] = None
    back_section_file_paths: Optional[List[str]] = None
