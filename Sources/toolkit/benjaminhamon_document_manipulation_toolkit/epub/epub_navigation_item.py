import dataclasses


@dataclasses.dataclass(frozen = True)
class EpubNavigationItem:
    reference: str
    display_name: str
