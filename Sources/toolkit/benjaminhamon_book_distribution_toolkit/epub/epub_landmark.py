import dataclasses


@dataclasses.dataclass(frozen = True)
class EpubLandmark:
    epub_type: str
    reference: str
    display_name: str
