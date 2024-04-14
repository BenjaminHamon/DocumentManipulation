""" Unit tests for document_operations """

from benjaminhamon_document_manipulation_toolkit.documents import document_operations


def test_generate_section_file_name():
    expected = "2 - My section title"
    actual = document_operations.generate_section_file_name("My section title", 1, 5)

    assert actual == expected

    expected = "02 - My section title"
    actual = document_operations.generate_section_file_name("My section title", 1, 10)

    assert actual == expected

    expected = "042 - My section title"
    actual = document_operations.generate_section_file_name("My section title", 41, 200)

    assert actual == expected
