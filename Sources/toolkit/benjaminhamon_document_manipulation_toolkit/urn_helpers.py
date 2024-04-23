import re


def convert_identifier_to_urn(identifier: str) -> str:
    isbn_match = re.search(r"^ISBN (?P<isbn>[0-9]+[ \-][0-9]+[ \-][0-9]+[ \-][0-9]+([ \-][0-9]+)?)$", identifier)
    if isbn_match is not None:
        return "urn:isbn:" + isbn_match.group("isbn").replace(" ", "").replace("-", "")

    raise ValueError("Unsupported identifier: '%s'" % identifier)
