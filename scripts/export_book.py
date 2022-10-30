import argparse
import logging
import os

import yaml
from ebooklib.epub import EpubWriter

from bhamon_book_distribution_toolkit.documents.document import Document
from bhamon_book_distribution_toolkit.documents.document_content import DocumentContent
from bhamon_book_distribution_toolkit.epub_converter import EpubConverter
from bhamon_book_distribution_toolkit.markdown_writer import MarkdownWriter
from bhamon_book_distribution_toolkit.odt_reader import OdtReader


logger = logging.getLogger("Main")


def main():
	logging.basicConfig(
		level = logging.INFO,
		style = "{",
		format = "{asctime} [{levelname}][{name}] {message}",
		datefmt = "%Y-%m-%dT%H:%M:%S")

	arguments = parse_arguments()
	configuration_file_path: str = os.path.normpath(arguments.configuration)
	document_repository = os.path.dirname(configuration_file_path)

	logger.info("Loading document configuration from '%s'", configuration_file_path)
	with open(configuration_file_path, mode = "r", encoding = "utf-8") as configuration_file:
		configuration = yaml.safe_load(configuration_file)

	text_source_file_path = os.path.normpath(os.path.join(document_repository, configuration["Resources"]["FullText"]))

	logger.info("Loading document metadata from '%s'", text_source_file_path)
	metadata = load_metadata(text_source_file_path)
	document = create_document(configuration, metadata)

	if arguments.annotation is not None:
		document.title += " - " + arguments.annotation.replace("{revision}", document.revision)

	logger.info("Loading document content from '%s'", text_source_file_path)
	document.content = load_content(text_source_file_path)

	output_file_path: str = os.path.normpath(arguments.output_file_path)
	logger.info("Writing document to '%s'", output_file_path)
	write_document(document, output_file_path)


def parse_arguments() -> argparse.Namespace:
	parser = argparse.ArgumentParser()
	parser.add_argument("configuration", help = "path to the configuration file")
	parser.add_argument("output_file_path", help = "path to the output file")
	parser.add_argument("--annotation", metavar = "<annotation>", help = "add an annotation to differentiate between several versions")
	return parser.parse_args()


def create_document(configuration: dict, metadata: dict) -> Document:
	return Document(
		identifier = configuration["Identifier"],
		title = configuration["Title"],
		authors = configuration["Authors"],
		language = configuration.get("Language", None),
		identifier_for_epub = configuration.get("IdentifierForEpub", None),
		revision = str(metadata["revision"]),
		revision_date = metadata["update_date"])


def load_metadata(text_source_file_path: str):
	if text_source_file_path.endswith(".fodt"):
		odt_reader = OdtReader({})
		odt_content = odt_reader.read_fodt(text_source_file_path)
		odt_metadata = odt_reader.read_metadata(odt_content)
		return odt_metadata

	if text_source_file_path.endswith(".odt"):
		odt_reader = OdtReader({})
		odt_content = odt_reader.read_odt(text_source_file_path, "meta.xml")
		odt_metadata = odt_reader.read_metadata(odt_content)
		return odt_metadata

	raise ValueError("File is unsupported: '%s'" % text_source_file_path)


def load_content(text_source_file_path: str) -> DocumentContent:
	if text_source_file_path.endswith(".fodt"):
		style_map = {
			"Custom - Chapter Body": "chapter-body",
			"Custom - Chapter Body Separator": "chapter-body-separator",
			"Custom - Chapter Hint": "chapter-hint",
			"Custom - Character Thoughts": "character-thoughts",
			"Custom - Journal Entry Header": "journal-entry-header",
			"Custom - Journal Entry": "journal-entry",
		}

		odt_reader = OdtReader(style_map)
		odt_content = odt_reader.read_fodt(text_source_file_path)
		return odt_reader.read_document_content(odt_content)

	if text_source_file_path.endswith(".odt"):
		style_map = {
			"Custom - Chapter Body": "chapter-body",
			"Custom - Chapter Body Separator": "chapter-body-separator",
			"Custom - Chapter Hint": "chapter-hint",
			"Custom - Character Thoughts": "character-thoughts",
			"Custom - Journal Entry Header": "journal-entry-header",
			"Custom - Journal Entry": "journal-entry",
		}

		odt_reader = OdtReader(style_map)
		odt_content = odt_reader.read_odt(text_source_file_path, "content.xml")
		return odt_reader.read_document_content(odt_content)

	raise ValueError("File is unsupported: '%s'" % text_source_file_path)


def write_document(document: Document, output_file_path: str) -> None:
	if output_file_path.endswith(".epub"):
		epub_converter = EpubConverter()
		document_as_epub = epub_converter.convert_document(document, "styles/book.css")
		epub = EpubWriter(output_file_path, document_as_epub)
		epub.process()
		epub.write()
		return

	if output_file_path.endswith(".md"):
		markdown_writer = MarkdownWriter()
		with open(output_file_path, mode = "w", encoding = "utf-8") as output_file:
			markdown_writer.write_document(output_file, document)
		return

	raise ValueError("File is unsupported: '%s'" % output_file_path)


if __name__ == "__main__":
	main()
