""" Unit tests for EpubPackageDocument """

import pytest

from benjaminhamon_book_distribution_toolkit.epub.epub_manifest_item import EpubManifestItem
from benjaminhamon_book_distribution_toolkit.epub.epub_package_document import EpubPackageDocument
from benjaminhamon_book_distribution_toolkit.epub.epub_spine_item import EpubSpineItem


def test_add_manifest_item():
    document = EpubPackageDocument()

    first_item = EpubManifestItem(
        identifier = "id1",
        reference = "file_1.xhtml",
        media_type = "application/xhtml+xml",
    )

    second_item = EpubManifestItem(
        identifier = "id2",
        reference = "file_2.xhtml",
        media_type = "application/xhtml+xml",
    )

    third_item = EpubManifestItem(
        identifier = "id3",
        reference = "file_3.xhtml",
        media_type = "application/xhtml+xml",
    )

    document.add_manifest_item(first_item)
    document.add_manifest_item(second_item)
    document.add_manifest_item(third_item)

    assert document.get_manifest_items() == [ first_item, second_item, third_item ]


def test_add_manifest_item_with_conflict():
    document = EpubPackageDocument()

    first_item = EpubManifestItem(
        identifier = "id1",
        reference = "file_1.xhtml",
        media_type = "application/xhtml+xml",
    )

    second_item = EpubManifestItem(
        identifier = "id1",
        reference = "file_2.xhtml",
        media_type = "application/xhtml+xml",
    )

    document.add_manifest_item(first_item)
    with pytest.raises(ValueError):
        document.add_manifest_item(second_item)


def test_set_manifest_item_as_navigation():
    document = EpubPackageDocument()

    toc_item = EpubManifestItem(
        identifier = "toc",
        reference = "toc.xhtml",
        media_type = "application/xhtml+xml",
    )

    document.add_manifest_item(toc_item)
    document.set_manifest_item_as_navigation(toc_item.identifier)

    assert toc_item.properties == [ "nav" ]


def test_set_manifest_item_as_navigation_with_missing():
    document = EpubPackageDocument()

    with pytest.raises(ValueError):
        document.set_manifest_item_as_navigation("missing")


def test_set_manifest_item_as_cover_image():
    document = EpubPackageDocument()

    toc_item = EpubManifestItem(
        identifier = "cover",
        reference = "cover.jpeg",
        media_type = "image/jpeg",
    )

    document.add_manifest_item(toc_item)
    document.set_manifest_item_as_cover_image(toc_item.identifier)

    assert toc_item.properties == [ "cover-image" ]


def test_set_manifest_item_as_cover_image_with_missing():
    document = EpubPackageDocument()

    with pytest.raises(ValueError):
        document.set_manifest_item_as_navigation("missing")


def test_add_spine_item():
    document = EpubPackageDocument()

    manifest_item = EpubManifestItem(
        identifier = "id1",
        reference = "file_1.xhtml",
        media_type = "application/xhtml+xml",
    )

    spine_item = EpubSpineItem(
        reference = manifest_item.identifier,
    )

    document.add_manifest_item(manifest_item)
    document.add_spine_item(spine_item)

    assert document.get_manifest_items() == [ manifest_item ]
    assert document.get_spine_items() == [ spine_item ]


def test_add_spine_item_with_missing():
    document = EpubPackageDocument()

    spine_item = EpubSpineItem(
        reference = "missing" ,
    )

    with pytest.raises(ValueError):
        document.add_spine_item(spine_item)
