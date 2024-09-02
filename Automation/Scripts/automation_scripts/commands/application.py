# cspell:words pyinstaller

import argparse
import logging
import os
import platform
from typing import Callable, List

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.automation.automation_command_group import AutomationCommandGroup
from bhamon_development_toolkit.processes.process_runner import ProcessRunner
from bhamon_development_toolkit.processes.process_spawner import ProcessSpawner
from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.configuration.project_configuration import ProjectConfiguration
from automation_scripts.configuration.project_environment import ProjectEnvironment
from automation_scripts.toolkit.python import python_helpers
from automation_scripts.toolkit.python.pyinstaller_runner import PyInstallerRunner
from automation_scripts.toolkit.python.python_application_builder import PythonApplicationBuilder


logger = logging.getLogger("Main")


class ApplicationCommand(AutomationCommandGroup):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        local_parser: argparse.ArgumentParser = subparsers.add_parser("application", help = "execute commands related to the application")

        command_collection: List[Callable[[],AutomationCommand]] = [
            _BuildBinariesCommand,
        ]

        self.add_commands(local_parser, command_collection)

        return local_parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


class _BuildBinariesCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        return subparsers.add_parser("build-binaries", help = "build the application binaries")


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        raise NotImplementedError("Not supported")


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        project_configuration: ProjectConfiguration = kwargs["configuration"]
        project_environment: ProjectEnvironment = kwargs["environment"]

        application_configuration_identifier = platform.system()
        output_directory = os.path.join("Artifacts", "Binaries", application_configuration_identifier)
        intermediate_directory = os.path.join("Artifacts", "Binaries-Intermediate", application_configuration_identifier)
        log_file_path = os.path.join("Artifacts", "Logs", "PyInstaller_%s.log" % application_configuration_identifier)

        python_system_executable = project_environment.get_python_system_executable()
        pyinstaller_venv_directory = os.path.join(intermediate_directory, ".venv")
        application_builder = self._create_application_builder(pyinstaller_venv_directory)

        all_python_packages = project_configuration.list_python_packages()

        if not simulate:
            if os.path.exists(output_directory):
                shutil.rmtree(output_directory)
            os.makedirs(output_directory)

        # Set up a new virtual environment since pyinstaller fails to discover editable installs when using pyproject.toml
        # See https://github.com/pyinstaller/pyinstaller/issues/7524
        self._setup_virtual_environment(python_system_executable, pyinstaller_venv_directory, all_python_packages, simulate = simulate)

        await application_builder.build_application(
            application_source_file_path = project_configuration.get_application_module_path(),
            executable_name = project_configuration.project_identifier,
            output_directory = output_directory,
            intermediate_directory = intermediate_directory,
            application_metadata = project_configuration.get_application_metadata(),
            log_file_path = log_file_path,
            simulate = simulate)


    def _create_application_builder(self, pyinstaller_venv_directory: str) -> PythonApplicationBuilder:
        pyinstaller_executable = python_helpers.get_venv_executable(pyinstaller_venv_directory, "pyinstaller")
        process_runner = ProcessRunner(ProcessSpawner(is_console = True))
        pyinstaller_runner = PyInstallerRunner(process_runner, pyinstaller_executable)
        return PythonApplicationBuilder(pyinstaller_runner)


    def _setup_virtual_environment(self,
            python_system_executable: str, pyinstaller_venv_directory: str, all_python_packages: List[PythonPackage], simulate: bool) -> None:

        pyinstaller_venv_executable = python_helpers.get_venv_python_executable(pyinstaller_venv_directory)

        python_helpers.setup_virtual_environment(python_system_executable, pyinstaller_venv_directory, simulate = simulate)
        python_helpers.install_python_packages(pyinstaller_venv_executable, [ "pyinstaller ~= 6.10.0" ], simulate = simulate)

        python_package_path_collection = [ python_package.path_to_sources for python_package in all_python_packages ]
        python_helpers.install_python_packages(pyinstaller_venv_executable, python_package_path_collection, simulate = simulate)
