""" Unit tests for EpubContentXhtmlBuilder """

# cspell:words lxml

import os
import platform

import lxml.etree
import pytest

from benjaminhamon_document_manipulation_toolkit.epub.epub_content_xhtml_builder import EpubContentXhtmlBuilder


def test_constructor():
    builder = EpubContentXhtmlBuilder("The Title")

    write_options = {
        "encoding": "utf-8",
        "pretty_print": True,
        "doctype": "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
    }

    xml_actual = lxml.etree.tostring(builder.get_xhtml_document(), **write_options).decode("utf-8")

    xml_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>The Title</title>
  </head>
  <body/>
</html>
"""

    xml_expected = xml_expected.lstrip()

    assert xml_actual == xml_expected


def test_add_style_sheet():
    builder = EpubContentXhtmlBuilder("The Title")
    builder.add_style_sheet(os.path.join("..", "Styles", "Generic.css"))

    write_options = {
        "encoding": "utf-8",
        "pretty_print": True,
        "doctype": "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
    }

    xml_actual = lxml.etree.tostring(builder.get_xhtml_document(), **write_options).decode("utf-8")

    xml_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>The Title</title>
    <link href="../Styles/Generic.css" rel="stylesheet" type="text/css"/>
  </head>
  <body/>
</html>
"""

    xml_expected = xml_expected.lstrip()

    assert xml_actual == xml_expected


def test_update_links():
    builder = EpubContentXhtmlBuilder("The Title")
    builder.add_style_sheet(os.path.join("..", "Styles", "Generic.css"))
    builder.update_links(os.path.join("Sources", "Xhtml", "File.xhtml"), os.path.join("Artifacts", "File.xhtml"))

    write_options = {
        "encoding": "utf-8",
        "pretty_print": True,
        "doctype": "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
    }

    xml_actual = lxml.etree.tostring(builder.get_xhtml_document(), **write_options).decode("utf-8")

    xml_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>The Title</title>
    <link href="../Sources/Styles/Generic.css" rel="stylesheet" type="text/css"/>
  </head>
  <body/>
</html>
"""

    xml_expected = xml_expected.lstrip()

    assert xml_actual == xml_expected


@pytest.mark.skipif(platform.system() != "Windows", reason = "Windows only")
def test_update_links_with_different_mount():
    builder = EpubContentXhtmlBuilder("The Title")
    builder.add_style_sheet(os.path.join("..", "Styles", "Generic.css"))

    with pytest.raises(ValueError):
        builder.update_links(os.path.join("Y:", "Sources", "Xhtml", "File.xhtml"), os.path.join("Z:", "Artifacts", "File.xhtml"))
