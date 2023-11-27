from typing import Dict


def format_text(source_text: str, parameters: Dict[str,str]) -> str:
    try:
        return source_text.format(**parameters)
    except KeyError as exception:
        raise KeyError("Parameter '%s' is required" % exception.args[0]) from exception
