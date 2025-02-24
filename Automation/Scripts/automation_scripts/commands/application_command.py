# cspell:words pyinstaller

import argparse
import logging
import os
import platform
import shutil
from typing import List

from bhamon_development_toolkit.automation.automation_command import AutomationCommand
from bhamon_development_toolkit.automation.automation_command_group import AutomationCommandGroup
from bhamon_development_toolkit.processes.process_runner import ProcessRunner
from bhamon_development_toolkit.processes.process_spawner import ProcessSpawner
from bhamon_development_toolkit.python import python_helpers
from bhamon_development_toolkit.python.pyinstaller_runner import PyInstallerRunner
from bhamon_development_toolkit.python.python_application_builder import PythonApplicationBuilder
from bhamon_development_toolkit.python.python_environment import PythonEnvironment
from bhamon_development_toolkit.python.python_package import PythonPackage
from bhamon_development_toolkit.security.interactive_credentials_provider import InteractiveCredentialsProvider

from automation_scripts.configuration.automation_configuration import AutomationConfiguration
from automation_scripts.toolkit.web.web_client import WebClient


logger = logging.getLogger("Main")


class ApplicationCommand(AutomationCommandGroup):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        local_parser: argparse.ArgumentParser = subparsers.add_parser("application", help = "execute commands related to the application")

        command_collection = [
            _BuildBinariesCommand,
            _StageForPackageCommand,
            _CreatePackageCommand,
            _UploadPackageCommand,
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
        automation_configuration: AutomationConfiguration = kwargs["configuration"]

        application_configuration_identifier = platform.system()
        output_directory = os.path.join("Artifacts", "Binaries", application_configuration_identifier)
        intermediate_directory = os.path.join("Artifacts", "Binaries-Intermediate", application_configuration_identifier)
        log_file_path = os.path.join("Artifacts", "Logs", "PyInstaller_%s.log" % application_configuration_identifier)

        pyinstaller_venv_directory = os.path.join(intermediate_directory, ".venv")
        application_builder = self._create_application_builder(pyinstaller_venv_directory)

        if not simulate:
            if os.path.exists(output_directory):
                shutil.rmtree(output_directory)
            os.makedirs(output_directory)

        # Set up a new virtual environment since pyinstaller fails to discover editable installs when using pyproject.toml
        # See https://github.com/pyinstaller/pyinstaller/issues/7524
        self._setup_virtual_environment(
            pyinstaller_venv_directory, automation_configuration.python_development_configuration.package_collection, simulate = simulate)

        application_module_path \
            = automation_configuration.application_development_configuration.get_module_path(automation_configuration.python_development_configuration)
        application_metadata = automation_configuration.application_development_configuration.get_metadata(automation_configuration.project_metadata)

        await application_builder.build_application(
            application_source_file_path = application_module_path,
            executable_name = automation_configuration.project_metadata.identifier,
            output_directory = output_directory,
            intermediate_directory = intermediate_directory,
            application_metadata = application_metadata,
            log_file_path = log_file_path,
            simulate = simulate)


    def _create_application_builder(self, pyinstaller_venv_directory: str) -> PythonApplicationBuilder:
        python_system_executable = python_helpers.resolve_system_python_executable()
        python_environment = PythonEnvironment(python_system_executable, pyinstaller_venv_directory)
        pyinstaller_executable = python_environment.get_venv_executable("pyinstaller")
        process_runner = ProcessRunner(ProcessSpawner(is_console = True))
        pyinstaller_runner = PyInstallerRunner(process_runner, pyinstaller_executable)
        return PythonApplicationBuilder(pyinstaller_runner)


    def _setup_virtual_environment(self, pyinstaller_venv_directory: str, all_python_packages: List[PythonPackage], simulate: bool) -> None:
        python_system_executable = python_helpers.resolve_system_python_executable()
        python_environment = PythonEnvironment(python_system_executable, pyinstaller_venv_directory)
        package_collection_for_pip = [ python_package.path_to_sources for python_package in all_python_packages ]

        python_environment.setup_virtual_environment(simulate = simulate)
        python_environment.install_python_packages([ "pyinstaller ~= 6.10.0" ], simulate = simulate)
        python_environment.install_python_packages(package_collection_for_pip, simulate = simulate)


class _StageForPackageCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("stage-for-package", help = "stage the files for the application package")
        parser.add_argument("--configuration", default = platform.system() + "Application",
            metavar = "<configuration>", help = "set the application package configuration")
        return parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        automation_configuration: AutomationConfiguration = kwargs["configuration"]
        application_configuration_identifier: str = arguments.configuration

        application_configuration \
            = automation_configuration.application_development_configuration.get_package_configuration(application_configuration_identifier)
        staging_directory = os.path.join("Artifacts", "Distributions-Staging", application_configuration_identifier)

        if not simulate:
            if os.path.exists(staging_directory):
                shutil.rmtree(staging_directory)
            os.makedirs(staging_directory)

        all_files_exist = True
        for source, _ in application_configuration.files_to_include:
            if not os.path.isfile(source):
                all_files_exist = False
                logger.error("File not found: '%s'", source)
        if not all_files_exist:
            raise FileNotFoundError("Some files were not found")

        logger.info("Copying files to '%s'", staging_directory)
        for source, destination in application_configuration.files_to_include:
            destination = os.path.join(staging_directory, destination)
            logger.debug("+ %s => %s", source, destination)
            if not simulate:
                os.makedirs(os.path.dirname(destination), exist_ok = True)
                shutil.copy(source, destination)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)


class _CreatePackageCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("create-package", help = "create the application package")
        parser.add_argument("--configuration", default = platform.system() + "Application",
            metavar = "<configuration>", help = "set the application package configuration")
        return parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        automation_configuration: AutomationConfiguration = kwargs["configuration"]
        application_configuration_identifier: str = arguments.configuration

        staging_directory = os.path.join("Artifacts", "Distributions-Staging", application_configuration_identifier)
        package_name = application_configuration_identifier + "_" + automation_configuration.project_metadata.version.full_identifier
        package_path = os.path.join("Artifacts", "Distributions", package_name)

        logger.info("Creating application package (Configuration: '%s')", application_configuration_identifier)

        shutil.make_archive(package_path + ".tmp", "zip", staging_directory, dry_run = simulate)
        if not simulate:
            os.replace(package_path + ".tmp.zip", package_path + ".zip")

        logger.debug("Package path: '%s'", package_path + ".zip")


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)


class _UploadPackageCommand(AutomationCommand):


    def configure_argument_parser(self, subparsers: argparse._SubParsersAction, **kwargs) -> argparse.ArgumentParser:
        parser = subparsers.add_parser("upload-package", help = "upload the application package")
        parser.add_argument("--configuration", default = platform.system() + "Application",
            metavar = "<configuration>", help = "set the application package configuration")
        return parser


    def check_requirements(self, arguments: argparse.Namespace, **kwargs) -> None:
        pass


    def run(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None: # pylint: disable = too-many-locals
        automation_configuration: AutomationConfiguration = kwargs["configuration"]
        application_configuration_identifier: str = arguments.configuration

        package_name = application_configuration_identifier + "_" + automation_configuration.project_metadata.version.full_identifier
        package_path = os.path.join("Artifacts", "Distributions", package_name + ".zip")

        artifact_parameters = automation_configuration.get_artifact_default_parameters()
        artifact_parameters["configuration"] = application_configuration_identifier
        artifact_name = "{project}_{version}+{revision}_{configuration}".format(**artifact_parameters)
        artifact_path = os.path.join("Artifacts", "Repository", artifact_name + ".zip")

        logger.info("Copying to local artifact repository")
        logger.debug("+ %s => %s", package_path, artifact_path)

        if not simulate:
            os.makedirs(os.path.dirname(artifact_path), exist_ok = True)
            shutil.copy(package_path, artifact_path + ".tmp")
            os.replace(artifact_path + ".tmp", artifact_path)

        repository_url = automation_configuration.workspace_environment.get_application_package_repository_url()
        repository_url += "/" + automation_configuration.project_metadata.identifier
        artifact_remote_url = repository_url + "/" + artifact_name + ".zip"

        credentials_provider = InteractiveCredentialsProvider()
        credentials = credentials_provider.get_credentials(repository_url)
        web_client = WebClient(authentication = (credentials.username, credentials.secret))

        logger.info("Uploading to remote repository (URL: '%s')", repository_url)
        if not simulate:
            web_client.upload_file(artifact_remote_url, artifact_path)
        logger.debug("Application package URL: '%s'", artifact_remote_url)


    async def run_async(self, arguments: argparse.Namespace, simulate: bool, **kwargs) -> None:
        self.run(arguments, simulate = simulate, **kwargs)
