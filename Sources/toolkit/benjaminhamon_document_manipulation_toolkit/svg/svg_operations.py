# cspell:words lxml svglib

import logging
import os
from typing import Optional

import lxml.etree
from reportlab.graphics import renderPM
import svglib.svglib


logger = logging.getLogger("SvgOperations")


def write_to_file(output_file_path: str, svg_as_xml: lxml.etree._ElementTree, encoding: Optional[str] = None, simulate: bool = False) -> None:
    logger.debug("Writing '%s'", output_file_path)

    if encoding is None:
        encoding = "utf-8"

    write_options = {
        "encoding": encoding,
        "pretty_print": True,
        "doctype": "<?xml version=\"1.0\" encoding=\"%s\"?>" % encoding,
    }

    svg_as_xml_string = lxml.etree.tostring(svg_as_xml, **write_options).decode(encoding)

    if not simulate:
        with open(output_file_path + ".tmp", mode = "w", encoding = encoding) as output_file:
            output_file.write(svg_as_xml_string)
        os.replace(output_file_path + ".tmp", output_file_path)


def convert_to_image(output_file_path: str, svg_as_xml: lxml.etree._ElementTree, source_file_path: str, image_format: str, simulate: bool = False) -> None:
    svg_renderer = svglib.svglib.SvgRenderer(source_file_path)
    drawing = svg_renderer.render(svg_as_xml.getroot())

    if not simulate:
        renderPM.drawToFile(drawing, output_file_path, fmt = image_format.upper())
