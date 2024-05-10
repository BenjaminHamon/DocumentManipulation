import os
import zipfile

from benjaminhamon_document_manipulation_scripts.create_epub_package import create_epub_package


def test_create_epub_package(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    staging_directory = os.path.join(workspace_directory, "Staging")
    package_file_path = os.path.join(workspace_directory, "Document.epub")

    _setup_workspace(workspace_directory)

    create_epub_package(
        source_directory = staging_directory,
        destination_file_path = package_file_path,
        simulate = False,
    )

    _assert_output(package_file_path)


def test_create_epub_package_with_simulate(tmpdir):
    workspace_directory = os.path.join(tmpdir, "Workspace")
    staging_directory = os.path.join(workspace_directory, "Staging")
    package_file_path = os.path.join(workspace_directory, "Document.epub")

    _setup_workspace(workspace_directory)

    create_epub_package(
        source_directory = staging_directory,
        destination_file_path = package_file_path,
        simulate = True,
    )

    assert not os.path.exists(package_file_path)


def _setup_workspace(workspace_directory: str) -> None:
    staging_directory = os.path.join(workspace_directory, "Staging")

    os.makedirs(staging_directory)
    os.makedirs(os.path.join(staging_directory, "EPUB"))

    for file_number in [ 1, 2, 3 ]:
        content_file_path = os.path.join(staging_directory, "EPUB", "File%s.xhtml" % file_number)
        with open(content_file_path, mode = "w", encoding = "utf-8") as content_file:
            content_file.write("")


def _assert_output(package_file_path: str) -> None:
    assert os.path.exists(package_file_path)

    file_collection_expected = [
        "EPUB/File1.xhtml",
        "EPUB/File2.xhtml",
        "EPUB/File3.xhtml",
        "mimetype",
    ]

    with zipfile.ZipFile(package_file_path, mode = "r") as package_file:
        assert package_file.testzip() is None

        file_collection = [ x.filename for x in package_file.filelist ]
        file_collection.sort()

        assert file_collection == file_collection_expected

        mimetype_data = package_file.read("mimetype").decode("utf-8")

        assert mimetype_data == "application/epub+zip"
