import argparse
import logging
import sys

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.processes.process_runner import ProcessRunner
from bhamon_development_toolkit.processes.process_spawner import ProcessSpawner
from bhamon_development_toolkit.python import python_helpers

from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.toolkit.python.python_package_builder import PythonPackageBuilder


logger = logging.getLogger("Main")


class DevelopCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("develop", help = "setup the python packages for development")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        python_executable = sys.executable
        project_configuration: ProjectConfiguration = kwargs["configuration"]
        all_python_packages = project_configuration.list_python_packages()

        process_runner = ProcessRunner(ProcessSpawner(is_console = True))
        python_package_builder = PythonPackageBuilder(python_executable, process_runner)

        logger.info("Generating python package metadata")
        for python_package in all_python_packages:
            python_package_builder.generate_package_metadata(
                product_identifier = project_configuration.project_identifier,
                project_version = project_configuration.project_version,
                copyright_text = project_configuration.copyright,
                python_package = python_package,
                simulate = simulate)

        logger.info("Installing python packages")
        python_package_path_collection = [ python_package.path_to_sources for python_package in all_python_packages ]
        python_helpers.install_python_packages(python_executable, python_package_path_collection, simulate = arguments.simulate)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
