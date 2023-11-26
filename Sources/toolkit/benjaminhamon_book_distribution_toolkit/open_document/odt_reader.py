# cspell:words dateutil fodt localname lxml nsmap

import datetime
import zipfile

import dateutil.parser
import lxml.etree


class OdtReader:


    def __init__(self, xml_parser: lxml.etree.XMLParser) -> None:
        self._xml_parser = xml_parser


    def read_fodt(self, odt_file_path: str) -> bytes:
        with open(odt_file_path, mode = "rb") as fodt_file:
            return fodt_file.read()


    def read_odt(self, odt_file_path: str, content_file_path: str) -> bytes:
        with zipfile.ZipFile(odt_file_path, mode = "r") as odt_file:
            return odt_file.read(content_file_path)


    def read_metadata(self, odt_content: bytes) -> dict:
        odt_as_xml = lxml.etree.fromstring(odt_content, self._xml_parser)
        metadata_as_xml = odt_as_xml.find("office:meta", namespaces = odt_as_xml.nsmap) # type: ignore

        if metadata_as_xml is None:
            raise ValueError("Metadata element not found")

        metadata = {}

        for item_as_xml in metadata_as_xml.iter():
            key = lxml.etree.QName(item_as_xml).localname
            value = item_as_xml.text

            if key == "meta" or value is None:
                continue

            if key == "title":
                metadata["title"] = value

            if key == "creator":
                metadata["author"] = value

            if key == "creation-date":
                metadata["creation_date"] = dateutil.parser.parse(value).astimezone(datetime.timezone.utc).replace(microsecond = 0)

            if key == "date":
                metadata["update_date"] = dateutil.parser.parse(value).astimezone(datetime.timezone.utc).replace(microsecond = 0)

            if key == "editing-cycles":
                metadata["revision"] = int(value)

            if key == "user-defined":
                continue

        return metadata
