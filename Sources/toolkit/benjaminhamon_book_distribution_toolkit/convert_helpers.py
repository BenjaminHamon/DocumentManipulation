import re


def sanitize_for_file_name(identifier: str) -> str:
    identifier = identifier.replace("’", "'")
    return re.sub(r"[^a-zA-Z0-9 \.\-_',]", "_", identifier)


def sanitize_for_file_name_and_href(identifier: str) -> str:
    identifier = identifier.replace("\\", "/")
    return re.sub(r"[^a-zA-Z0-9\.\-_/]", "_", identifier)


def sanitize_for_identifier(identifier: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "_", identifier)
