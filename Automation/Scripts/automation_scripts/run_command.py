import argparse
import logging
import sys
from typing import List

from bhamon_development_toolkit.asyncio_extensions.asyncio_context import AsyncioContext
from bhamon_development_toolkit.automation.automation_command import AutomationCommand

from automation_scripts.commands.application_command import ApplicationCommand
from automation_scripts.commands.clean_command import CleanCommand
from automation_scripts.commands.develop_command import DevelopCommand
from automation_scripts.commands.distribution_command import DistributionCommand
from automation_scripts.commands.info_command import InfoCommand
from automation_scripts.commands.lint_command import LintCommand
from automation_scripts.commands.test_command import TestCommand
from automation_scripts.configuration import configuration_manager
from automation_scripts.helpers import automation_helpers


logger = logging.getLogger("Main")


def main():
    with automation_helpers.execute_in_workspace(__file__):
        configuration = configuration_manager.load_automation_configuration()
        command_collection = create_command_collection()

        argument_parser = create_argument_parser(command_collection)
        arguments = argument_parser.parse_args()
        command_instance: AutomationCommand = arguments.command_instance

        automation_helpers.configure_logging(arguments)

        automation_helpers.log_script_information(configuration.project_metadata, arguments.simulate)
        command_instance.check_requirements(arguments, configuration = configuration)

        asyncio_context = AsyncioContext()
        asyncio_context.run(command_instance.run_async(arguments, configuration = configuration, simulate = arguments.simulate))


def create_argument_parser(command_collection: List[AutomationCommand]) -> argparse.ArgumentParser:
    main_parser = automation_helpers.create_argument_parser()

    subparsers = main_parser.add_subparsers(title = "commands", metavar = "<command>")
    subparsers.required = True

    for command_instance in command_collection:
        command_parser = command_instance.configure_argument_parser(subparsers)
        command_parser.set_defaults(command_instance = command_instance)

    return main_parser


def create_command_collection() -> List[AutomationCommand]:
    return [
        ApplicationCommand(),
        CleanCommand(),
        DevelopCommand(),
        DistributionCommand(),
        InfoCommand(),
        LintCommand(),
        TestCommand(),
    ]


if __name__ == "__main__":
    try:
        main()
    except Exception: # pylint: disable = broad-except
        logger.error("Script failed", exc_info = True)
        sys.exit(1)
