# cspell:words levelname

import logging


all_logging_levels = [ "debug", "info", "warning", "error", "critical" ]


def get_logging_level_as_integer(level_as_string: str) -> int:
    if level_as_string.lower() == "debug":
        return logging.DEBUG
    if level_as_string.lower() == "info":
        return logging.INFO
    if level_as_string.lower() == "warning":
        return logging.WARNING
    if level_as_string.lower() == "error":
        return logging.ERROR
    if level_as_string.lower() == "critical":
        return logging.CRITICAL

    raise ValueError("Unknown logging level '%s'" % level_as_string)


def configure_logging(verbosity: str) -> None:
    logging.basicConfig(
        level = get_logging_level_as_integer(verbosity),
        format = "[{levelname}][{name}] {message}",
        datefmt = "%Y-%m-%dT%H:%M:%S",
        style = "{")
