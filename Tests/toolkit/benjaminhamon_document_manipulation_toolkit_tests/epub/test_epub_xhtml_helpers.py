# cspell:words lxml

""" Unit tests for epub_xhtml_helpers """

import io

import lxml.etree
import pytest

from benjaminhamon_document_manipulation_toolkit.epub import epub_xhtml_helpers


def test_create_xhtml_base():
    document = epub_xhtml_helpers.create_xhtml_base("The Title")

    document_as_string_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head>
    <title>The Title</title>
  </head>
  <body/>
</html>
"""

    document_as_string_expected = document_as_string_expected.lstrip()
    document_as_string = lxml.etree.tostring(document,
        doctype = "<?xml version=\"1.0\" encoding=\"utf-8\"?>", encoding = "utf-8", pretty_print = True).decode("utf-8")

    assert document_as_string == document_as_string_expected


def test_find_xhtml_element():
    document_as_string = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
  <head/>
  <body/>
</html>
"""

    document_as_string = document_as_string.lstrip()
    document = lxml.etree.parse(io.BytesIO(document_as_string.encode("utf-8")))

    epub_xhtml_helpers.find_xhtml_element(document.getroot(), "./x:head")
    with pytest.raises(ValueError):
        epub_xhtml_helpers.find_xhtml_element(document.getroot(), "./x:something")
