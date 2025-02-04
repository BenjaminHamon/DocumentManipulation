""" Unit tests for HtmlWriter """

import os

import lxml.html.html5parser

from benjaminhamon_document_manipulation_toolkit.documents import document_element_factory
from benjaminhamon_document_manipulation_toolkit.documents.elements.root_element import RootElement
from benjaminhamon_document_manipulation_toolkit.html.document_to_html_converter import DocumentToHtmlConverter
from benjaminhamon_document_manipulation_toolkit.html.html_writer import HtmlWriter


def create_document() -> RootElement:
    document = RootElement()

    document.children.append(
        document_element_factory.create_section(
            heading = "Section 1",
            text = [
                [ "Some text for the first section." ],
                [ "And a second paragraph for the first section." ]
            ],
        )
    )

    document.children.append(
        document_element_factory.create_section(
            heading = "Section 2",
            text = [
                [ "Some text for the second section." ],
                [ "And a second paragraph for the second section." ]
            ],
        )
    )

    return document


def test_write_as_single_document(tmpdir):
    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_writer = HtmlWriter(DocumentToHtmlConverter(), html_parser)

    metadata = { "author": "The Author" }
    document = create_document()
    css_file_path = os.path.join(tmpdir, "Sources", "Styles.css")
    html_file_path = os.path.join(tmpdir, "Working", "MyDocument.html")

    os.makedirs(os.path.dirname(html_file_path))
    html_writer.write_as_single_document(html_file_path, "The Title", metadata, document, css_file_path = css_file_path, simulate = False)

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>The Title</title>
    <link href="../Sources/Styles.css" rel="stylesheet" type="text/css"/>
    <meta name="author" content="The Author"/>
  </head>
  <body>
    <section>
      <h1>
        <p>The Title</p>
      </h1>
      <section>
        <h2>
          <span>Section 1</span>
        </h2>
        <p>
          <span>Some text for the first section.</span>
        </p>
        <p>
          <span>And a second paragraph for the first section.</span>
        </p>
      </section>
      <section>
        <h2>
          <span>Section 2</span>
        </h2>
        <p>
          <span>Some text for the second section.</span>
        </p>
        <p>
          <span>And a second paragraph for the second section.</span>
        </p>
      </section>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_single_document_with_template(tmpdir):
    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_writer = HtmlWriter(DocumentToHtmlConverter(), html_parser)

    metadata = { "author": "The Author" }
    document = create_document()
    template_file_path = os.path.join(tmpdir, "Sources", "Template.html")
    html_file_path = os.path.join(tmpdir, "Working", "MyDocument.html")

    template_content = """
<!doctype html>
<html>
  <head>
    <title></title>
    <link href="Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
  </body>
</html>
"""

    template_content = template_content.lstrip()

    os.makedirs(os.path.dirname(template_file_path))
    with open(template_file_path, mode = "w", encoding = "utf-8") as template_file:
        template_file.write(template_content)

    os.makedirs(os.path.dirname(html_file_path))
    html_writer.write_as_single_document(html_file_path, "The Title", metadata, document, template_file_path = template_file_path, simulate = False)

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>The Title</title>
    <link href="../Sources/Styles.css" rel="stylesheet" type="text/css"/>
    <meta name="author" content="The Author"/>
  </head>
  <body>
    <section>
      <h1>
        <p>The Title</p>
      </h1>
      <section>
        <h2>
          <span>Section 1</span>
        </h2>
        <p>
          <span>Some text for the first section.</span>
        </p>
        <p>
          <span>And a second paragraph for the first section.</span>
        </p>
      </section>
      <section>
        <h2>
          <span>Section 2</span>
        </h2>
        <p>
          <span>Some text for the second section.</span>
        </p>
        <p>
          <span>And a second paragraph for the second section.</span>
        </p>
      </section>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_single_document_with_simulate(tmpdir):
    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_writer = HtmlWriter(DocumentToHtmlConverter(), html_parser)

    metadata = { "author": "The Author" }
    document = create_document()
    html_file_path = os.path.join(tmpdir, "Working", "MyDocument.html")

    html_writer.write_as_single_document(html_file_path, "The Title", metadata, document, simulate = True)

    assert not os.path.exists(html_file_path)


def test_write_as_many_documents(tmpdir):
    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_writer = HtmlWriter(DocumentToHtmlConverter(), html_parser)

    metadata = { "author": "The Author" }
    document = create_document()
    css_file_path = os.path.join(tmpdir, "Sources", "Styles.css")
    html_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(html_directory)
    html_writer.write_as_many_documents(html_directory, metadata, document, css_file_path = css_file_path, simulate = False)

    assert len(os.listdir(html_directory)) == 2

    html_file_path = os.path.join(html_directory, "1 - Section 1.html")

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>Section 1</title>
    <link href="../../Sources/Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <section>
      <h1>
        <span>Section 1</span>
      </h1>
      <p>
        <span>Some text for the first section.</span>
      </p>
      <p>
        <span>And a second paragraph for the first section.</span>
      </p>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    html_file_path = os.path.join(html_directory, "2 - Section 2.html")

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>Section 2</title>
    <link href="../../Sources/Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <section>
      <h1>
        <span>Section 2</span>
      </h1>
      <p>
        <span>Some text for the second section.</span>
      </p>
      <p>
        <span>And a second paragraph for the second section.</span>
      </p>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_many_documents_with_template(tmpdir):
    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_writer = HtmlWriter(DocumentToHtmlConverter(), html_parser)

    metadata = { "author": "The Author" }
    document = create_document()
    information_template_file_path = os.path.join(tmpdir, "Sources", "InformationTemplate.html")
    section_template_file_path = os.path.join(tmpdir, "Sources", "SectionTemplate.html")
    html_directory = os.path.join(tmpdir, "Working", "MyDocument")

    os.makedirs(os.path.join(tmpdir, "Sources"))

    section_template_content = """
<!doctype html>
<html>
  <head>
    <title></title>
    <link href="Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
  </body>
</html>
"""

    section_template_content = section_template_content.lstrip()

    with open(section_template_file_path, mode = "w", encoding = "utf-8") as template_file:
        template_file.write(section_template_content)

    information_template_content = """
<!doctype html>
<html>
  <head>
    <title></title>
    <link href="Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <p>{author}</p>
  </body>
</html>
"""

    with open(information_template_file_path, mode = "w", encoding = "utf-8") as template_file:
        template_file.write(information_template_content)

    os.makedirs(html_directory)
    html_writer.write_as_many_documents(html_directory, metadata, document,
        section_template_file_path = section_template_file_path, information_template_file_path = information_template_file_path, simulate = False)

    assert len(os.listdir(html_directory)) == 3

    html_file_path = os.path.join(html_directory, "0 - Information.html")

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>Information</title>
    <link href="../../Sources/Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <p>The Author</p>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    html_file_path = os.path.join(html_directory, "1 - Section 1.html")

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>Section 1</title>
    <link href="../../Sources/Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <section>
      <h1>
        <span>Section 1</span>
      </h1>
      <p>
        <span>Some text for the first section.</span>
      </p>
      <p>
        <span>And a second paragraph for the first section.</span>
      </p>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content

    html_file_path = os.path.join(html_directory, "2 - Section 2.html")

    assert os.path.exists(html_file_path)

    with open(html_file_path, mode = "r", encoding = "utf-8") as html_file:
        actual_content = html_file.read()

    expected_content = """
<!doctype html>
<html>
  <head>
    <title>Section 2</title>
    <link href="../../Sources/Styles.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <section>
      <h1>
        <span>Section 2</span>
      </h1>
      <p>
        <span>Some text for the second section.</span>
      </p>
      <p>
        <span>And a second paragraph for the second section.</span>
      </p>
    </section>
  </body>
</html>
"""

    expected_content = expected_content.lstrip()

    assert actual_content == expected_content


def test_write_as_many_documents_with_simulate(tmpdir):
    html_parser = lxml.html.html5parser.HTMLParser(namespaceHTMLElements = False)
    html_writer = HtmlWriter(DocumentToHtmlConverter(), html_parser)

    metadata = { "author": "The Author" }
    document = create_document()
    html_directory = os.path.join(tmpdir, "Working", "MyDocument")

    html_writer.write_as_many_documents(html_directory, metadata, document, simulate = True)

    assert not os.path.exists(html_directory)
