# cspell:words fodt

import dataclasses
from typing import Optional


@dataclasses.dataclass()
class MarkdownToOdtConfiguration:

    # Content conversion
    fodt_template_file_path: Optional[str] = None
    style_map_file_path: Optional[str] = None
