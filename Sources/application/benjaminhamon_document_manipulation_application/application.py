import argparse
import logging
import os
import sys
from typing import List

import benjaminhamon_document_manipulation_application
from benjaminhamon_document_manipulation_application import application_helpers
from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand
from benjaminhamon_document_manipulation_application.asyncio_extensions.asyncio_context import AsyncioContext

logger = logging.getLogger("Main")


def main() -> None:
    command_collection = list_commands()

    argument_parser = create_argument_parser(command_collection)
    arguments = argument_parser.parse_args()
    command_instance: ApplicationCommand = arguments.command_instance

    application_helpers.configure_logging(arguments)

    log_script_information(simulate = arguments.simulate)
    command_instance.check_requirements(arguments)

    asyncio_context = AsyncioContext()
    asyncio_context.run(command_instance.run_async(arguments, simulate = arguments.simulate))


def create_argument_parser(command_collection: List[str]) -> argparse.ArgumentParser:
    main_parser = application_helpers.create_argument_parser()

    subparsers = main_parser.add_subparsers(title = "commands", metavar = "<command>")
    subparsers.required = True

    for command in command_collection:
        command_instance = application_helpers.create_command_instance(command)
        command_parser = command_instance.configure_argument_parser(subparsers)
        command_parser.set_defaults(command_instance = command_instance)

    return main_parser


def log_script_information(simulate: bool = False) -> None:
    if simulate:
        logger.info("(( The script is running as a simulation ))")
        logger.info("")

    application_title = benjaminhamon_document_manipulation_application.__product__
    application_version = benjaminhamon_document_manipulation_application.__version__

    logger.debug("%s %s", application_title, application_version)
    logger.debug("Executing in '%s'", os.getcwd())
    logger.debug("")


def list_commands() -> List[str]:
    return [
        "benjaminhamon_document_manipulation_application.commands.info_command.InfoCommand",
    ]


if __name__ == "__main__":
    try:
        main()
    except Exception: # pylint: disable = broad-except
        logger.error("Script failed", exc_info = True)
        sys.exit(1)
