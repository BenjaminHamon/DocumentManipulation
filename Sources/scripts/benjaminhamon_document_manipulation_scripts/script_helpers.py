# cspell:words levelname

import logging


all_logging_levels = [ "debug", "info", "warning", "error", "critical" ]


def configure_logging(verbosity: str) -> None:
    logging.basicConfig(
        level = logging.getLevelName(verbosity.upper()),
        format = "[{levelname}][{name}] {message}",
        datefmt = "%Y-%m-%dT%H:%M:%S",
        style = "{")
