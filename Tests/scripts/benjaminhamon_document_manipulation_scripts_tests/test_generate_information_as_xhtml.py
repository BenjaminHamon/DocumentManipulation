# cspell:words dcterms fodt idref itemref oebps opendocument relators rootfile rootfiles

import datetime
import os

from benjaminhamon_document_manipulation_scripts.generate_information_as_xhtml import create_serializer
from benjaminhamon_document_manipulation_scripts.generate_information_as_xhtml import generate_information_as_xhtml


def test_generate_information_as_xhtml(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    information_file_path = os.path.join(workspace_directory, "Information.yaml")
    template_file_path = os.path.join(workspace_directory, "InformationTemplate.xhtml")
    output_file_path = os.path.join(workspace_directory, "Information.xhtml")

    _setup_workspace(workspace_directory)

    generate_information_as_xhtml(
        serializer = create_serializer("yaml"),
        information_file_path = information_file_path,
        dc_metadata_file_path = None,
        destination_file_path = output_file_path,
        template_file_path = template_file_path,
        revision_control = None,
        extra_information = {},
        now = datetime.datetime(2020, 1, 1, tzinfo = datetime.timezone.utc),
        simulate = False,
    )

    _assert_output(workspace_directory)


def test_generate_information_as_xhtml_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    information_file_path = os.path.join(workspace_directory, "Information.yaml")
    template_file_path = os.path.join(workspace_directory, "InformationTemplate.xhtml")
    output_file_path = os.path.join(workspace_directory, "Information.xhtml")

    _setup_workspace(workspace_directory)

    generate_information_as_xhtml(
        serializer = create_serializer("yaml"),
        information_file_path = information_file_path,
        dc_metadata_file_path = None,
        destination_file_path = output_file_path,
        template_file_path = template_file_path,
        revision_control = None,
        extra_information = {},
        now = datetime.datetime(2020, 1, 1, tzinfo = datetime.timezone.utc),
        simulate = True,
    )

    assert not os.path.exists(output_file_path)


def _setup_workspace(workspace_directory: str) -> None:

    def create_information() -> None:
        information_file_path = os.path.join(workspace_directory, "Information.yaml")

        information_data = """
title: "Some Title"
author: "Some Author"
publisher: "Some Publisher"
version_identifier: "1.0.0"
copyright: "Copyright © 2020 Some Author"
"""

        information_data = information_data.lstrip()

        with open(information_file_path, mode = "w", encoding = "utf-8") as information_file:
            information_file.write(information_data)

    def create_template() -> None:
        template_file_path = os.path.join(workspace_directory, "InformationTemplate.xhtml")

        template_data = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Information</title>
  </head>
  <body>
    <section id="book-information">
      <div id="title-information">
        <div class="book-title">{title}</div>
        <div class="book-author">written by {author}</div>
      </div>
      <div id="edition-information">
        <div>Draft {date}</div>
      </div>
      <div id="version-information">
        <div>Version {version_identifier}</div>
      </div>
      <div id="copyright-notice">
        <div>{copyright}</div>
        <div>All rights reserved</div>
      </div>
    </section>
  </body>
</html>
"""

        template_data = template_data.lstrip()

        with open(template_file_path, mode = "w", encoding = "utf-8") as template_file:
            template_file.write(template_data)

    os.makedirs(workspace_directory)

    create_information()
    create_template()


def _assert_output(workspace_directory: str) -> None: # pylint: disable = too-many-locals
    output_file_path = os.path.join(workspace_directory, "Information.xhtml")

    with open(output_file_path, mode = "r", encoding = "utf-8") as xhtml_file:
        xhtml_data = xhtml_file.read()

    xhtml_data_expected = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Information</title>
  </head>
  <body>
    <section id="book-information">
      <div id="title-information">
        <div class="book-title">Some Title</div>
        <div class="book-author">written by Some Author</div>
      </div>
      <div id="edition-information">
        <div>Draft 01-Jan-2020</div>
      </div>
      <div id="version-information">
        <div>Version 1.0.0</div>
      </div>
      <div id="copyright-notice">
        <div>Copyright © 2020 Some Author</div>
        <div>All rights reserved</div>
      </div>
    </section>
  </body>
</html>
"""

    xhtml_data_expected = xhtml_data_expected.lstrip()

    assert xhtml_data == xhtml_data_expected
