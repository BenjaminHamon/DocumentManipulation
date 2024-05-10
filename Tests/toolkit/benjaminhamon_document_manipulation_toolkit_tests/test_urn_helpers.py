from benjaminhamon_document_manipulation_toolkit import urn_helpers


def test_convert_identifier_to_urn_with_isbn():
    isbn = "ISBN 81-7525-766-0" # 10-digit ISBN with dashes
    urn_actual = urn_helpers.convert_identifier_to_urn(isbn)
    urn_expected = "urn:isbn:8175257660"
    assert urn_actual == urn_expected

    isbn = "ISBN 81 7525 766 0" # 10-digit ISBN with spaces
    urn_actual = urn_helpers.convert_identifier_to_urn(isbn)
    urn_expected = "urn:isbn:8175257660"
    assert urn_actual == urn_expected

    isbn = "ISBN 978-81-7525-766-5" # 10-digit ISBN with dashes
    urn_actual = urn_helpers.convert_identifier_to_urn(isbn)
    urn_expected = "urn:isbn:9788175257665"
    assert urn_actual == urn_expected

    isbn = "ISBN 978 81 7525 766 5" # 10-digit ISBN with spaces
    urn_actual = urn_helpers.convert_identifier_to_urn(isbn)
    urn_expected = "urn:isbn:9788175257665"
    assert urn_actual == urn_expected
