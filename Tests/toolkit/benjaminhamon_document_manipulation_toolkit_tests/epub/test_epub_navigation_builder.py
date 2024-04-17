""" Unit tests for EpubNavigationBuilder """

# cspell:words bodymatter lxml

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.epub.epub_landmark import EpubLandmark
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_builder import EpubNavigationBuilder
from benjaminhamon_document_manipulation_toolkit.epub.epub_navigation_item import EpubNavigationItem


def test_empty():
    navigation_builder = EpubNavigationBuilder("Table of Contents")

    document_as_string_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Table of Contents</title>
  </head>
  <body/>
</html>
"""

    document_as_string_expected = document_as_string_expected.lstrip()

    document = navigation_builder.get_xhtml_document()
    document_as_string = lxml.etree.tostring(document,
        doctype = "<?xml version=\"1.0\" encoding=\"utf-8\"?>", encoding = "utf-8", pretty_print = True).decode("utf-8")

    assert document_as_string == document_as_string_expected


def test_full():
    navigation_builder = EpubNavigationBuilder("Table of Contents")

    navigation_builder.add_table_of_contents([
        EpubNavigationItem("my_first_section.xhtml", "My first section"),
        EpubNavigationItem("my_second_section.xhtml", "My second section"),
    ])

    navigation_builder.add_landmarks([
        EpubLandmark("toc", "toc.xhtml", "Table of Contents"),
        EpubLandmark("bodymatter", "my_first_section.xhtml", "Start of Content"),
    ])


    document_as_string_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>Table of Contents</title>
  </head>
  <body>
    <nav epub:type="toc">
      <h1>Table of Contents</h1>
      <ol>
        <li>
          <a href="my_first_section.xhtml">My first section</a>
        </li>
        <li>
          <a href="my_second_section.xhtml">My second section</a>
        </li>
      </ol>
    </nav>
    <nav epub:type="landmarks">
      <h1>Landmarks</h1>
      <ol>
        <li>
          <a epub:type="toc" href="toc.xhtml">Table of Contents</a>
        </li>
        <li>
          <a epub:type="bodymatter" href="my_first_section.xhtml">Start of Content</a>
        </li>
      </ol>
    </nav>
  </body>
</html>
"""

    document_as_string_expected = document_as_string_expected.lstrip()

    document = navigation_builder.get_xhtml_document()
    document_as_string = lxml.etree.tostring(document,
        doctype = "<?xml version=\"1.0\" encoding=\"utf-8\"?>", encoding = "utf-8", pretty_print = True).decode("utf-8")

    assert document_as_string == document_as_string_expected
