# cspell:words lxml opendocument

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.open_document import odt_operations
from benjaminhamon_document_manipulation_toolkit.open_document.odt_builder_for_copies import OdtBuilderForCopies

def test_add_copies():
    odt_as_bytes = """
<?xml version="1.0" encoding="utf-8"?>
<office:document
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <draw:frame draw:name="image" text:anchor-type="page" text:anchor-page-number="1"/>
      <text:h>A title</text:h>
      <text:p>Some text</text:p>
      <text:p>{code}</text:p>
    </office:text>
  </office:body>
</office:document>
    """

    odt_as_bytes = odt_as_bytes.lstrip().encode("utf-8")

    xml_parser = lxml.etree.XMLParser(encoding = "utf-8", remove_blank_text = True)
    odt_as_xml = lxml.etree.ElementTree(lxml.etree.fromstring(odt_as_bytes, xml_parser))

    new_document = odt_operations.create_document()
    odt_builder = OdtBuilderForCopies(new_document)
    odt_builder.add_copies(odt_as_xml, [ { "code": "aaa" }, { "code": "bbb" }, { "code": "ccc" }])

    new_document = odt_builder.get_xml_document()
    new_document_as_string = lxml.etree.tostring(new_document, pretty_print = True).decode("utf-8").strip()

    expected = """
<office:document xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:text>
      <draw:frame draw:name="image-1" text:anchor-type="page" text:anchor-page-number="1"/>
      <draw:frame draw:name="image-2" text:anchor-type="page" text:anchor-page-number="2"/>
      <draw:frame draw:name="image-3" text:anchor-type="page" text:anchor-page-number="3"/>
      <text:h>A title</text:h>
      <text:p>Some text</text:p>
      <text:p>aaa</text:p>
      <text:h>A title</text:h>
      <text:p>Some text</text:p>
      <text:p>bbb</text:p>
      <text:h>A title</text:h>
      <text:p>Some text</text:p>
      <text:p>ccc</text:p>
    </office:text>
  </office:body>
</office:document>
    """

    expected = expected.strip()

    assert new_document_as_string == expected
