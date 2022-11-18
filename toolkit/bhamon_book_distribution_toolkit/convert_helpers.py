import re


def sanitize_identifier_for_file_name(identifier: str) -> str:
	identifier = identifier.replace("’", "'")
	return re.sub(r"[^a-zA-Z0-9 \.\-_',]", "_", identifier)
