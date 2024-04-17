# cspell:words iterchildren lxml nsmap

import lxml.etree

from benjaminhamon_document_manipulation_toolkit.open_document import odt_operations


def test_remove_content():
    odt_document = odt_operations.create_document()
    odt_body = odt_operations.get_body_text_element(odt_document)

    paragraph_element = lxml.etree.SubElement(odt_body, lxml.etree.QName(odt_body.nsmap["text"], "p"))
    paragraph_element.text = "Some text"

    paragraph_element = lxml.etree.SubElement(odt_body, lxml.etree.QName(odt_body.nsmap["text"], "p"))
    paragraph_element.text = "And some more text"

    paragraph_element = lxml.etree.SubElement(odt_body, lxml.etree.QName(odt_body.nsmap["text"], "p"))
    paragraph_element.text = "And even more text"

    assert sum(1 for _ in odt_body.iterchildren()) == 3

    odt_operations.remove_content(odt_document)

    assert sum(1 for _ in odt_body.iterchildren()) == 0
