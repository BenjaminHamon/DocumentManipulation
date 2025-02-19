import argparse
from typing import Callable, List

from benjaminhamon_document_manipulation_application.application_command import ApplicationCommand


class ApplicationCommandGroup(ApplicationCommand):


    def add_commands(self, parser: argparse.ArgumentParser, command_factory_collection: List[Callable[[],ApplicationCommand]]) -> None:
        subparsers = parser.add_subparsers(title = "commands", metavar = "<command>")
        subparsers.required = True

        for command in command_factory_collection:
            command_instance = command()
            command_parser = command_instance.configure_argument_parser(subparsers)
            command_parser.set_defaults(command_instance = command_instance)


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Run is not supported for a command group")


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Run is not supported for a command group")
