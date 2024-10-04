# cspell:words fodt

import dataclasses
from typing import List, Optional, Tuple

from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.epub.epub_metadata_item import EpubMetadataItem


@dataclasses.dataclass()
class OdtToEpubConfiguration: # pylint: disable = too-many-instance-attributes

    # Document information
    information_file_path: Optional[str] = None
    dc_metadata_file_path: Optional[str] = None
    extra_metadata: Optional[List[EpubMetadataItem]] = None
    revision_control: Optional[str] = None
    xhtml_information_template_file_path: Optional[str] = None

    # Sources
    source_file_path: Optional[str] = None
    source_section_regex: Optional[str] = None
    fodt_template_file_path: Optional[str] = None
    cover_file: Optional[str] = None
    cover_svg_template_file_path: Optional[str] = None

    # Content conversion
    xhtml_section_template_file_path: Optional[str] = None
    style_sheet_file_path: Optional[str] = None
    style_map_file_path: Optional[str] = None

    # Package
    content_files_before: List[str] = dataclasses.field(default_factory = list)
    content_files_after: List[str] = dataclasses.field(default_factory = list)
    resource_files: List[str] = dataclasses.field(default_factory = list)
    link_overrides: List[Tuple[str,str]] = dataclasses.field(default_factory = list)
    landmarks: List[EpubLandmark] = dataclasses.field(default_factory = list)
