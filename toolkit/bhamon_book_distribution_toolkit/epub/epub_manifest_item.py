import dataclasses


@dataclasses.dataclass(frozen = True)
class EpubManifestItem:
	identifier: str
	source_file_path: str
	path_relative_to_opf: str
	media_type: str
