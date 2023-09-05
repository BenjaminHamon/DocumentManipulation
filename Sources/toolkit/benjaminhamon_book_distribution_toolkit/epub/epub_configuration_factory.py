from benjaminhamon_book_distribution_toolkit.epub.epub_metadata_item import EpubMetadataItem
from benjaminhamon_book_distribution_toolkit.epub.epub_metadata_refine import EpubMetadataRefine


def create_metadata_item(metadata_item_as_dict) -> EpubMetadataItem:
    return EpubMetadataItem(
        key = metadata_item_as_dict["key"],
        value = metadata_item_as_dict["value"],
        is_meta = metadata_item_as_dict.get("is_meta", False),
        xhtml_identifier = metadata_item_as_dict.get("xhtml_identifier", None),
        refine_collection = [ create_metadata_refine(metadata_refine_as_dict) for metadata_refine_as_dict in metadata_item_as_dict.get("refines", []) ])


def create_metadata_refine(metadata_refine_as_dict) -> EpubMetadataRefine:
    return EpubMetadataRefine(
        key = metadata_refine_as_dict["key"],
        value = metadata_refine_as_dict["value"],
        scheme = metadata_refine_as_dict.get("scheme", None),
    )
